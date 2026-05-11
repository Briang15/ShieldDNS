const AD_SELECTORS = [
  '.ad-showing',
  '.ad-interrupting',
  '#player-ads',
  '#masthead-ad',
  '.ytp-ad-overlay-container',
  '.ytp-ad-text-overlay',
  '.ytp-ad-skip-button',
  '.ytp-skip-ad-button',
  '#promoted-videos',
  'ytd-promoted-sparkles-web-renderer',
  'ytd-promoted-video-renderer',
  'ytd-display-ad-renderer',
  'ytd-banner-promo-renderer',
  'ytd-statement-banner-renderer',
  'ytd-ad-slot-renderer',
  'ytd-in-feed-ad-layout-renderer',
  'ytd-search-pyv-renderer',
  'ytd-masthead-ad',
  '.ytd-rich-item-renderer[is-ad]',
]

let active = true

function removeAds() {
  if (!active) return

  AD_SELECTORS.forEach(selector => {
    document.querySelectorAll(selector).forEach(el => el.remove())
  })

  const skipBtn = document.querySelector('.ytp-ad-skip-button, .ytp-skip-ad-button')
  if (skipBtn) skipBtn.click()

  const video = document.querySelector('video')
  if (video && document.querySelector('.ad-showing')) {
    video.currentTime = video.duration
  }
}

// Listen for toggle from background
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.action === 'disable') active = false
  if (msg.action === 'enable')  active = true
})

// Load saved state on startup
chrome.storage.local.get('enabled', (data) => {
  active = data.enabled !== false
})

removeAds()
setInterval(removeAds, 300)

const observer = new MutationObserver(removeAds)
observer.observe(document.documentElement, { childList: true, subtree: true })
