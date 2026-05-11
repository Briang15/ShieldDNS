let blockedCount = 0

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ enabled: true })
  chrome.action.setBadgeText({ text: '0' })
  chrome.action.setBadgeBackgroundColor({ color: '#a6e3a1' })
})

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.action === 'disable') {
    chrome.declarativeNetRequest.updateEnabledRulesets({
      disableRulesetIds: ['block_ads']
    })
    chrome.action.setBadgeText({ text: 'OFF' })
    chrome.action.setBadgeBackgroundColor({ color: '#f38ba8' })
    chrome.tabs.query({ url: '*://*.youtube.com/*' }, (tabs) => {
      tabs.forEach(tab => chrome.tabs.sendMessage(tab.id, { action: 'disable' }))
    })
  }

  if (msg.action === 'enable') {
    chrome.declarativeNetRequest.updateEnabledRulesets({
      enableRulesetIds: ['block_ads']
    })
    chrome.action.setBadgeText({ text: String(blockedCount) })
    chrome.action.setBadgeBackgroundColor({ color: '#a6e3a1' })
    chrome.tabs.query({ url: '*://*.youtube.com/*' }, (tabs) => {
      tabs.forEach(tab => chrome.tabs.sendMessage(tab.id, { action: 'enable' }))
    })
  }
})
