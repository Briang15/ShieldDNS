; ShieldDNS Installer
; Built with NSIS

!define APP_NAME "ShieldDNS"
!define APP_VERSION "1.0"
!define INSTALL_DIR "$PROGRAMFILES\ShieldDNS"

Name "${APP_NAME} ${APP_VERSION}"
OutFile "ShieldDNS_Setup.exe"
InstallDir "${INSTALL_DIR}"
RequestExecutionLevel admin

; Modern UI
!include "MUI2.nsh"

!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Custom colors
!define MUI_BGCOLOR "1E1E2E"
!define MUI_TEXTCOLOR "CDD6F4"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ── Welcome Page Text
!define MUI_WELCOMEPAGE_TITLE "Welcome to ShieldDNS"
!define MUI_WELCOMEPAGE_TEXT "ShieldDNS blocks ads and trackers system-wide on Windows and in Chrome including YouTube.$\r$\n$\r$\nThis installer will:$\r$\n$\r$\n  • Install the ShieldDNS host blocker (256,000+ domains)$\r$\n  • Install the Chrome extension files$\r$\n  • Create a desktop shortcut$\r$\n$\r$\nClick Next to continue."

; ── Finish Page
!define MUI_FINISHPAGE_TITLE "ShieldDNS Installed"
!define MUI_FINISHPAGE_TEXT "ShieldDNS has been installed.$\r$\n$\r$\nTo complete setup:$\r$\n$\r$\n1. Run ShieldDNS from your desktop to enable host blocking$\r$\n2. Open Chrome and go to chrome://extensions$\r$\n3. Enable Developer Mode and click Load Unpacked$\r$\n4. Select: $INSTDIR\extension$\r$\n$\r$\nClick Finish to exit."
!define MUI_FINISHPAGE_RUN "$INSTDIR\ShieldDNS.bat"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ShieldDNS now"

Section "MainSection" SEC01

  SetOutPath "$INSTDIR"

  ; ── Core files
  SetOutPath "$INSTDIR\core\blocklists"
  File "core\blocklists\blocked_domains.txt"

  SetOutPath "$INSTDIR\core"
  File "core\update_blocklist.py"
  File "core\checker.py"

  ; ── Windows app
  SetOutPath "$INSTDIR\windows"
  File "windows\hosts_manager.py"

  ; ── Chrome extension
  SetOutPath "$INSTDIR\extension"
  File "extension\manifest.json"
  File "extension\background.js"
  File "extension\content.js"
  File "extension\popup.html"
  File "extension\popup.js"
  File "extension\rules.json"
  File "extension\icon.png"

  ; ── Launcher batch file
  SetOutPath "$INSTDIR"
  FileOpen $0 "$INSTDIR\ShieldDNS.bat" w
  FileWrite $0 "@echo off$\r$\n"
  FileWrite $0 "cd /d $\"%~dp0$\"$\r$\n"
  FileWrite $0 "python windows\hosts_manager.py$\r$\n"
  FileWrite $0 "pause$\r$\n"
  FileClose $0

  ; ── Desktop shortcut
  CreateShortCut "$DESKTOP\ShieldDNS.lnk" "$INSTDIR\ShieldDNS.bat" "" "$INSTDIR\ShieldDNS.bat"

  ; ── Start menu
  CreateDirectory "$SMPROGRAMS\ShieldDNS"
  CreateShortCut "$SMPROGRAMS\ShieldDNS\ShieldDNS.lnk" "$INSTDIR\ShieldDNS.bat"
  CreateShortCut "$SMPROGRAMS\ShieldDNS\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

  ; ── Uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; ── Registry entry for Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShieldDNS" \
    "DisplayName" "ShieldDNS"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShieldDNS" \
    "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShieldDNS" \
    "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShieldDNS" \
    "Publisher" "Briang15"

SectionEnd

Section "Uninstall"
  ; Remove files
  RMDir /r "$INSTDIR\core"
  RMDir /r "$INSTDIR\windows"
  RMDir /r "$INSTDIR\extension"
  Delete "$INSTDIR\ShieldDNS.bat"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"

  ; Remove shortcuts
  Delete "$DESKTOP\ShieldDNS.lnk"
  Delete "$SMPROGRAMS\ShieldDNS\ShieldDNS.lnk"
  Delete "$SMPROGRAMS\ShieldDNS\Uninstall.lnk"
  RMDir "$SMPROGRAMS\ShieldDNS"

  ; Remove registry
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShieldDNS"
SectionEnd
