const toggle = document.getElementById('main-toggle')
const label  = document.getElementById('status-label')
const features = ['f1','f2','f3','f4']

// Load saved state
chrome.storage.local.get('enabled', (data) => {
  const enabled = data.enabled !== false // default on
  toggle.checked = enabled
  updateUI(enabled)
})

// Update blocked count
chrome.action.getBadgeText({}, (text) => {
  document.getElementById('count').textContent = text || '0'
})

// Handle toggle
toggle.addEventListener('change', () => {
  const enabled = toggle.checked
  chrome.storage.local.set({ enabled })
  updateUI(enabled)

  // Tell background to enable/disable rules and content script
  chrome.runtime.sendMessage({ action: enabled ? 'enable' : 'disable' })
})

function updateUI(enabled) {
  if (enabled) {
    label.textContent = 'Protection Active'
    label.className = 'toggle-label on'
    features.forEach(id => {
      const el = document.getElementById(id)
      el.className = 'feature'
      el.querySelector('span').textContent = '✓'
    })
  } else {
    label.textContent = 'Protection Off'
    label.className = 'toggle-label off'
    features.forEach(id => {
      const el = document.getElementById(id)
      el.className = 'feature disabled'
      el.querySelector('span').textContent = '✗'
    })
  }
}
