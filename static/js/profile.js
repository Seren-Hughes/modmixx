/**
 * Profile page audio management
 *
 * Separate from feed.js = different audio management needs
 * - Feed has complex AudioManager class with infinite scroll and sticky player plans
 * - Profile just needs simple "one audio at a time" functionality
 * - Different pages, different audio features (feed has play/pause states, profile has edit/delete)
 * - Avoids conflicts between competing audio management systems
 */
document.addEventListener('DOMContentLoaded', function() {
    // Profile page audio management - only one track plays at a time
    const audioPlayers = document.querySelectorAll('audio');
    
    if (audioPlayers.length > 0) {
        audioPlayers.forEach(function(audio) {
            audio.addEventListener('play', function() {
                // When this audio starts playing, pause all others on profile page
                audioPlayers.forEach(function(otherAudio) {
                    if (otherAudio !== audio) {
                        otherAudio.pause();
                    }
                });
            });
        });
    }
});