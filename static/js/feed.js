/*
  Track Feed Infinite Scroll (5 items/page)

  Overview:
  - Uses IntersectionObserver to detect when the sentinel enters the viewport and
    fetches the next page of tracks from /tracks/feed-api/?page=N.
  - Assumes the first page of tracks is server-rendered (SSR) in the template; JS starts at page = 2.
  - Appends new track "cards" that match the existing Bootstrap layout.
  - Provides basic accessibility: screen-reader live region announces loads, and a "Back to top" button appears after scroll.

  Requirements in template (feed.html):
  - <div id="track-feed">…first page server-rendered…</div>
  - <div id="loading" style="display:none;"></div>
  - <div id="feed-sentinel"></div>
  - <div id="sr-announcer" class="visually-hidden" aria-live="polite" aria-atomic="true"></div>
  - <button id="backToTop" …>↑ Top</button>

  Backend API:
  - Endpoint: /tracks/feed-api/?page=N
  - Returns JSON: { tracks: [ … ], has_next: boolean }
  - Each track item includes fields used below (title, slug, detail_url, description, created_ago,
    audio_url, image_url, comment_count, profile{ username, display_name, url, avatar })

  Accessibility:
  - Announce new items via #sr-announcer (aria-live region).
  - Provide a visible “Back to top” button to help keyboard and screen-reader users.

  References:
  - MDN IntersectionObserver: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
  - Django Pagination: https://docs.djangoproject.com/en/stable/topics/pagination/
  - JsonResponse: https://docs.djangoproject.com/en/stable/ref/request-response/#jsonresponse-objects
*/

let page = 2; // Start at 2 because page 1 is server-rendered in the template
let loading = false;
let hasNext = true; // Will be updated by API responses

// Optionally derive hasNext from a data attribute exposed by the server if available.
function initialHasNextHint() {
  hasNext = true;
}

/**
 * Build avatar HTML. Uses profile avatar if present; falls back to initial badge.
 */
function buildAvatarHTML(profile) {
  if (profile.avatar) {
    return `<img src="${profile.avatar}" class="rounded-circle me-2" alt="${escapeHtml(profile.display_name)}" style="width:32px;height:32px;object-fit:cover">`;
  }
  const initial = (profile.display_name || profile.username || '?').trim().charAt(0).toUpperCase();
  return `<div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2" style="width:32px;height:32px">
            <span class="text-white" style="font-size:14px;">${escapeHtml(initial)}</span>
          </div>`;
}

/**
 * Build a Bootstrap card for a track.
 */
function buildCard(t) {
  const avatar = buildAvatarHTML(t.profile);
  const image = t.image_url
    ? `<img src="${t.image_url}" class="img-fluid rounded" alt="Uploaded track art work for ${escapeHtml(t.title)}" style="max-height:150px;object-fit:cover">`
    : `<div class="bg-light rounded d-flex align-items-center justify-content-center" style="height:150px"></div>`;
  const commentsText = t.comment_count === 0 ? 'No comments yet'
                    : t.comment_count === 1 ? '1 comment'
                    : `${t.comment_count} comments`;

  return `
    <div class="card mb-3">
      <div class="card-body">
        <div class="d-flex align-items-center mb-3">
          <a href="${t.profile.url}" class="text-decoration-none">
            ${avatar}
          </a>
          <div>
            <div>
              <a href="${t.profile.url}" class="text-decoration-none fw-semibold">
                ${escapeHtml(t.profile.display_name)}
              </a>
            </div>
            <small class="text-muted">${escapeHtml(t.created_ago)}</small>
          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            ${image}
          </div>
          <div class="col-md-9">
            <h5 class="card-title">
              <a href="${t.detail_url}" class="text-decoration-none">${escapeHtml(t.title)}</a>
            </h5>
            ${t.description ? `<p class="card-text">${escapeHtml(t.description)}</p>` : ''}
            <div class="mb-2">
              <audio controls class="w-100" style="max-width:400px;">
                <source src="${t.audio_url}" type="audio/mpeg">
              </audio>
            </div>
            <div class="mt-2">
              <a href="${t.detail_url}#comments" class="text-decoration-none text-muted">
                <i class="fa fa-comment me-1"></i>${commentsText}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

/**
 * Escape HTML to prevent XSS when rendering user-generated content.
 */
function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

/**
 * Fetch next page and append items. Announces count via #sr-announcer.
 */
async function loadMore() {
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

    let appended = 0;
    data.tracks.forEach(t => {
      container.insertAdjacentHTML('beforeend', buildCard(t));
      appended += 1;
    });

    hasNext = data.has_next;
    page += 1;

    // Announce to screen readers
    const announcer = document.getElementById('sr-announcer');
    if (announcer && appended > 0) {
      announcer.textContent = `Loaded ${appended} more tracks`;
    }

    //  announce end of feed
    if (!hasNext && announcer) {
      announcer.textContent = `${appended > 0 ? 'Loaded more tracks. ' : ''}End of feed.`;
    }
  } catch (e) {
    console.error(e);
    const announcer = document.getElementById('sr-announcer');
    if (announcer) announcer.textContent = 'Could not load more tracks. Please try again.';
  } finally {
    if (loadingEl) loadingEl.style.display = 'none';
    loading = false;
  }
}

/**
 * Initialize observer and UI behaviours.
 * Falls back gracefully if IntersectionObserver is unavailable.
 */
document.addEventListener('DOMContentLoaded', () => {
  initialHasNextHint();

  const sentinel = document.getElementById('feed-sentinel');

  if ('IntersectionObserver' in window && sentinel) {
    const io = new IntersectionObserver(
      entries => entries.forEach(entry => { if (entry.isIntersecting) loadMore(); }),
      { rootMargin: '200px' } // start loading a bit before the sentinel is fully visible
    );
    io.observe(sentinel);
  } else {
    // Fallback: load on scroll near bottom
    window.addEventListener('scroll', () => {
      if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
        loadMore();
      }
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
});