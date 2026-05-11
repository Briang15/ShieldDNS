const { app, BrowserWindow, ipcMain } = require('electron')
const { exec, spawn } = require('child_process')
const path = require('path')
const fs = require('fs')
const os = require('os')

let win

function createWindow() {
  win = new BrowserWindow({
    width: 600,
    height: 500,
    resizable: false,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    icon: path.join(__dirname, 'icon.png')
  })
  win.loadFile('index.html')
}

app.whenReady().then(createWindow)

// Close / minimize controls
ipcMain.on('close-app', () => app.quit())
ipcMain.on('minimize-app', () => win.minimize())

// Run the actual install
ipcMain.on('start-install', (event) => {
  const installDir = path.join(os.homedir(), 'ShieldDNS')
  const steps = []

  function send(msg, percent) {
    event.reply('install-progress', { msg, percent })
  }

  send('Creating installation directory...', 5)

  // Create folders
  const dirs = [
    installDir,
    path.join(installDir, 'core', 'blocklists'),
    path.join(installDir, 'windows'),
    path.join(installDir, 'extension'),
  ]
  dirs.forEach(d => fs.mkdirSync(d, { recursive: true }))

  send('Copying core files...', 20)

  // Source files are in the parent directory of the installer
  const src = path.join(__dirname, '..')

  const copies = [
    ['core/update_blocklist.py', 'core/update_blocklist.py'],
    ['core/checker.py', 'core/checker.py'],
    ['core/blocklists/blocked_domains.txt', 'core/blocklists/blocked_domains.txt'],
    ['windows/hosts_manager.py', 'windows/hosts_manager.py'],
    ['extension/manifest.json', 'extension/manifest.json'],
    ['extension/background.js', 'extension/background.js'],
    ['extension/content.js', 'extension/content.js'],
    ['extension/popup.html', 'extension/popup.html'],
    ['extension/popup.js', 'extension/popup.js'],
    ['extension/rules.json', 'extension/rules.json'],
  ]

  copies.forEach(([from, to]) => {
    const srcFile = path.join(src, from)
    const dstFile = path.join(installDir, to)
    if (fs.existsSync(srcFile)) {
      fs.copyFileSync(srcFile, dstFile)
    }
  })

  send('Copying extension files...', 50)

  // Create desktop shortcut batch file
  const batContent = `@echo off\ncd /d "${installDir}"\npython windows\\hosts_manager.py\npause\n`
  fs.writeFileSync(path.join(installDir, 'ShieldDNS.bat'), batContent)

  // Create desktop shortcut
  send('Creating desktop shortcut...', 70)
  const desktopShortcut = path.join(os.homedir(), 'Desktop', 'ShieldDNS.bat')
  fs.copyFileSync(path.join(installDir, 'ShieldDNS.bat'), desktopShortcut)

  send('Installing Python dependencies...', 85)
  exec('pip install requests', (err) => {
    if (err) {
      send('Warning: Could not install requests. Run: pip install requests', 90)
    }
    send('Installation complete!', 100)
    event.reply('install-done', { installDir })
  })
})
