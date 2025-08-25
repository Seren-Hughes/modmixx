/* jshint esversion: 11, esnext: false */
/*
  Track Feed Infinite Scroll & Audio Management

  - Loads more tracks from /tracks/feed-api/?page=N as you scroll (IntersectionObserver or scroll fallback)
  - Only one audio track plays at a time
  - Accessibility: screen reader announcements, "Back to top" button
  - First page is server-side rendered (SSR); JS loads from page 2 onward

  Backend API:
    /tracks/feed-api/?page=N (returns { tracks: [...], has_next: boolean })

  Template requirements:
    track-feed, loading, feed-sentinel, sr-announcer, backToTop

  References:
    - MDN IntersectionObserver: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
    - Django Pagination: https://docs.djangoproject.com/en/stable/topics/pagination/
    - JsonResponse: https://docs.djangoproject.com/en/stable/ref/request-response/#jsonresponse-objects
    - escapeHtml adapted from: https://stackoverflow.com/a/6234804
*/

/**
 * Track Feed with Audio Management
 * 
 * Features:
 * - Infinite scroll pagination (5 tracks per page)
 * - Single-track audio playback (automatically stops other tracks)
 * - Dynamic track loading with consistent behaviour
 * - Accessibility features (screen reader announcements, back to top)
 * 
 * API Integration:
 * - Fetches from /tracks/feed-api/?page=N
 * - Seamless integration between server-rendered and dynamic content
 */

// -------------   Global audio state management -------------
let currentAudio = null; // Currently playing audio element
let currentTrackSlug = null; // Slug of the currently playing track

// Get initial pagination info from the HTML template
const feedEl = document.getElementById('track-feed');
let hasNext = feedEl?.dataset.hasNext === 'true';  // Are there more pages to load?
let page = parseInt(feedEl?.dataset.nextPage || '2', 10);  // Next page number to fetch
let loading = false; // Prevent multiple API calls at once
let ioRef = null; // Reference to the IntersectionObserver (for cleanup)

// Keep track of which tracks already added to prevent duplicates
// This fixes the bug where the same tracks appeared multiple times
const seenSlugs = new Set();

// -------------------- Helper functions --------------------

/**
 * Escape HTML to prevent XSS attacks when showing user-generated content
 */
function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\'': '&#39;' }[c]));
}


/**
 * Build the user avatar HTML (profile pic or initial badge)
 */
function buildAvatarHTML(profile) {
  if (profile.avatar) {
    return `<img src="${profile.avatar}" class="rounded-circle me-2" alt="${escapeHtml(profile.display_name)}" style="width:32px;height:32px;object-fit:cover">`;
  }
  // Fallback: show first letter of display name in a circle
  const initial = (profile.display_name || profile.username || '?').trim().charAt(0).toUpperCase();
  return `<div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2" style="width:32px;height:32px">
            <span class="text-white" style="font-size:14px;">${escapeHtml(initial)}</span>
          </div>`;
}

/**
 * Truncate text to a specific word count (mimics Django's truncatewords filter)
 */
function truncateWords(text, wordCount = 10) {
  if (!text) return '';
  const words = text.trim().split(/\s+/);
  if (words.length <= wordCount) return text;
  return words.slice(0, wordCount).join(' ') + '…';
}

/**
 * Build a complete track card HTML
 * This matches the Django template for consistency 
 */
function buildCard(t) {
  const avatar = buildAvatarHTML(t.profile);
  const image = t.image_url ? `<img src="${t.image_url}" class="track-artwork" alt="Cover art for ${escapeHtml(t.title)}">` : `<div class="track-artwork-placeholder"><i class="fas fa-music"></i></div>`;

  // t.comment_count (from API) not t.visible_comment_count!
  const commentCount = t.comment_count || 0;
  const commentText = (commentCount === 0) ? 'No comments yet' : (commentCount === 1) ? '1 comment' : `${commentCount} comments`;

  return `
    <div class="card mb-3" data-track-slug="${t.slug}">
      <div class="card-body">
        <div class="track-card-body">
          ${image}
          <div class="track-content">
            <div class="track-profile-info">
              <div class="track-profile-left">
                <a href="${t.profile.url}" class="text-decoration-none">
                  ${avatar}
                </a>
                <a href="${t.profile.url}" class="text-decoration-none track-profile-name">${escapeHtml(t.profile.display_name)}</a>
              </div>
              <div class="track-profile-timestamp">
                <small class="text-muted">${escapeHtml(t.created_ago)}</small>
              </div>
            </div>
            <h5 class="track-title">
              <a href="${t.detail_url}" class="text-decoration-none">${escapeHtml(t.title)}</a>
            </h5>
            <p class="track-description">
              ${t.description ? truncateWords(escapeHtml(t.description), 10) : ''}
            </p>
            <div class="track-audio-section">
              <audio controls preload="metadata" class="w-100"
                     data-track-slug="${t.slug}"
                     aria-label="Play ${escapeHtml(t.title)} by ${escapeHtml(t.profile.display_name)}">
                <source src="${t.audio_url}" type="audio/mpeg">
              </audio>
              <div class="mt-2">
                <a href="${t.detail_url}#comments" class="text-decoration-none text-muted">
                  <i class="fa fa-comment me-1"></i>${commentText}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

/**
 * Attach play/pause event listeners to audio elements
 * Uses data-audio-bound to avoid adding listeners multiple times to the same element
 * This replaced the old inline onplay/onpause handlers for better security and maintainability
 * https://javascript.info/event-delegation
 */
function bindAudioEvents(root = document) {
  const audios = root.querySelectorAll('audio[data-track-slug]:not([data-audio-bound])');
  audios.forEach((audio) => {
    const slug = audio.dataset.trackSlug;
    audio.addEventListener('play', () => window.AudioManager?.handlePlay(slug, audio));
    audio.addEventListener('pause', () => window.AudioManager?.handlePause(slug, audio));
    audio.setAttribute('data-audio-bound', '1');  // Mark as processed
  });
}

// -------------------- Infinite scroll logic --------------------

/**
 * Fetch the next page of tracks and add them to the feed
 * Announce new tracks to screen readers (sr-announcer)
 * Only adds tracks not seen before (prevents duplicates)
 */
async function loadMore() {
  // Don't load if already loading or no more pages
  if (loading || !hasNext) return;
  loading = true;

  const loadingEl = document.getElementById('loading');
  if (loadingEl) loadingEl.style.display = 'block';

  try {
    const res = await fetch(`/tracks/feed-api/?page=${page}`, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) throw new Error('Network error');
    const data = await res.json();

    const container = document.getElementById('track-feed');
    if (!container) return;

    // Filter out tracks already shown (this was the key fix for duplicates!)
    const uniqueTracks = (data.tracks || []).filter(t => t?.slug && !seenSlugs.has(t.slug));
    
    // Add each new track to the page and remember
    uniqueTracks.forEach(t => {
      container.insertAdjacentHTML('beforeend', buildCard(t));
      seenSlugs.add(t.slug);  // Remember this track so it's not added again
    });

    // Set up audio event listeners for the new tracks
    bindAudioEvents(container);

    // Update pagination state
    hasNext = !!data.has_next;
    page += 1;

    // Announce to screen readers
    const announcer = document.getElementById('sr-announcer');
    if (announcer) {
      if (uniqueTracks.length > 0) announcer.textContent = `Loaded ${uniqueTracks.length} more tracks`;
      if (!hasNext) announcer.textContent = `${uniqueTracks.length > 0 ? 'Loaded more tracks. ' : ''}End of feed.`;
    }

    // Show end message if no more tracks
    if (!hasNext) {
  const endMessage = document.createElement('div');
  endMessage.className = 'text-center py-5';
  endMessage.innerHTML = `
    <div class="mb-3">
      <i class="fas fa-music text-muted" style="font-size: 2rem;"></i>
    </div>
    <h5 class="text-muted mb-2">You've heard all the mixx!</h5>
    <p class="text-muted mb-3">That's every track in the feed for now.</p>
    <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" 
           class="btn btn-outline-primary btn-sm">
      <i class="fas fa-arrow-up me-2"></i>Back to the top
    </button>
  `;
  container.appendChild(endMessage);
} else {
  console.log('Debug: Still has more tracks, hasNext =', hasNext);
}

    // Clean up: stop watching for scroll when done
    if (!hasNext && ioRef) {
      ioRef.disconnect();
      ioRef = null;
    }
  } catch (e) {
    console.error('Failed to load more tracks:', e);
    const announcer = document.getElementById('sr-announcer');
    if (announcer) announcer.textContent = 'Could not load more tracks. Please try again.';
  } finally {
    if (loadingEl) loadingEl.style.display = 'none';
    loading = false;
  }
}

// -------------------- Page initialization --------------------
document.addEventListener('DOMContentLoaded', () => {
  // Find all tracks that were rendered by Django (server-side) and remember their slugs
  // This prevents adding duplicates of tracks that are already on the page
  document.querySelectorAll('.card[data-track-slug]').forEach(el => {
    const slug = el.dataset.trackSlug;
    if (slug) seenSlugs.add(slug);
  });

  // Set up audio event listeners for tracks that were server-rendered
  bindAudioEvents(document);

  // Set up infinite scroll (only if there are more pages to load)
  const sentinel = document.getElementById('feed-sentinel');
  if (hasNext && 'IntersectionObserver' in window && sentinel) {
    // Load more when the sentinel comes into view 
    ioRef = new IntersectionObserver(
      entries => entries.forEach(entry => { if (entry.isIntersecting) loadMore(); }),
      { rootMargin: '200px' }  // Start loading 200px before sentinel is visible
    );
    ioRef.observe(sentinel);
  } else if (hasNext) {
    // Fallback for older browsers: load more when scrolled near bottom
    let scrollTimeout = null;
    window.addEventListener('scroll', () => {
      if (scrollTimeout) clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
          loadMore();
        }
      }, 100);
    });
  }

  // Back to top visibility + behaviour
  const backToTop = document.getElementById('backToTop');
  window.addEventListener('scroll', () => {
    if (!backToTop) return;
    backToTop.style.display = window.scrollY > 600 ? 'block' : 'none';
  });
  backToTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Show upload modal if ?share=1 is in the URL
  const params = new URLSearchParams(window.location.search);
  if (params.get('share') === '1') {
    const modal = document.getElementById('uploadModal');
    if (modal && window.bootstrap?.Modal) new bootstrap.Modal(modal).show();
  }
});

// -------------------- Audio playback management --------------------
/**
 * Manages audio playback so only one track plays at a time
 * When you play a new track, it automatically pauses the previous one
 */
class AudioManager {
  static handlePlay(trackSlug, audioElement) {
    // Stop whatever was playing before
    if (currentAudio && currentAudio !== audioElement) {
      currentAudio.pause();
      currentAudio.currentTime = 0;  // Reset to beginning
      this.updatePlayButtonState(currentTrackSlug, 'stopped');
    }
    
    // Update tracking of what's currently playing
    currentAudio = audioElement;
    currentTrackSlug = trackSlug;
    this.updatePlayButtonState(trackSlug, 'playing');
  }

  static handlePause(trackSlug, audioElement) {
    // Only update UI if this is the track playing
    if (currentAudio === audioElement) {
      this.updatePlayButtonState(trackSlug, 'paused');
    }
  }

  static updatePlayButtonState(trackSlug, state) {
    // Update play/pause buttons 
    const el = document.querySelector(`[data-track-slug="${trackSlug}"] .play-btn`);
    if (el) el.textContent = state === 'playing' ? 'Pause' : 'Play';
  }
}

// Make AudioManager available globally so the event handlers can find it
window.AudioManager = AudioManager;