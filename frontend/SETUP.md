# iOS Setup Guide

Step-by-step instructions to get the iOS app running.

## Prerequisites Check

1. **Xcode installed?**
   - Open Spotlight (⌘ + Space)
   - Type "Xcode"
   - If not installed, download from Mac App Store

2. **macOS version?**
   - Click Apple logo → About This Mac
   - Need macOS 14.0 or later

## Setup Steps

### Step 1: Navigate to iOS Directory
```bash
cd ~/Documents/ai-interactive-podcast/ios  # adjust path as needed
```

### Step 2: Open Project in Xcode
```bash
open AIPodcast.xcodeproj
```

Or double-click `AIPodcast.xcodeproj` in Finder.

### Step 3: Configure API Base URL

1. In Xcode, open `Utils/Constants.swift`
2. Find `apiBaseURL`
3. **For simulator:** Leave as `http://localhost:8000`
4. **For physical device:** Change to your Mac's IP address

To find your Mac's IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Update Constants.swift:
```swift
static let apiBaseURL = "http://192.168.1.XXX:8000"  // Use your actual IP
```

### Step 4: Select Target Device

In Xcode toolbar:
- Click device dropdown (next to scheme)
- Choose iPhone 15 Pro simulator (or your device if connected)

### Step 5: Build and Run

Click the Play button (▶️) or press ⌘ + R

First build takes 1-2 minutes.

## Verify It's Working

1. App should launch in simulator
2. You should see the main interface
3. Check Xcode console for any errors

## Troubleshooting

### Build Errors

**"No signing certificate found"**
1. Xcode → Settings → Accounts
2. Add your Apple ID
3. Select your team in project settings

**"Target iOS 17.0 not found"**
1. Xcode → Settings → Platforms
2. Download iOS 17.0+ SDK

### Runtime Errors

**"Failed to connect to API"**
1. Make sure backend is running:
```bash
   cd ../backend
   python main.py
```
2. Check `Constants.swift` has correct URL

**"Simulator won't launch"**
1. Xcode → Window → Devices and Simulators
2. Delete simulator and create new one
3. Try different simulator model

### Still Stuck?

1. Post in Slack group chat with:
   - Screenshot of error
   - What you were trying to do
   - What you've already tried

2. Schedule office hours with [Your Name]

## Next Steps

Once app is running:
1. Check your assigned tickets in Linear
2. Start with "iOS Setup" tickets
3. Read through the starter code to understand structure
4. Begin implementing your first feature!

## Tips

- **Build often** - Don't write too much code without testing
- **Use breakpoints** - Click line numbers to add breakpoints for debugging
- **Read console** - Xcode console shows helpful error messages
- **SwiftUI preview** - Use preview canvas to see changes without building