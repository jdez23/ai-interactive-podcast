# iOS Setup Guide

Step-by-step instructions for iOS engineers.

---

## Prerequisites Check

### Check macOS Version

Click Apple logo → About This Mac

**Need:** macOS 14.0 or later

### Check Xcode Installation

Open Spotlight (⌘ + Space), type "Xcode"

**If not installed:**
1. Open App Store
2. Search "Xcode"
3. Install (this takes a while - 10+ GB download)

**Check Xcode version:**
```bash
xcodebuild -version
```

**Need:** Xcode 15.0 or later

---

## Setup Steps

### Step 1: Navigate to AIPodcast Directory
```bash
# From project root
cd frontend/AIPodcast
```

### Step 2: Open Project in Xcode
```bash
# Open project
open AIPodcast.xcodeproj
```

Or double-click `AIPodcast.xcodeproj` in Finder.

**First time opening?** Xcode may:
- Index the project (1-2 minutes)
- Download additional components
- Ask to trust the developer

---

### Step 3: Configure API Base URL

The app needs to know where to find the backend API.

1. In Xcode, open `AIPodcast/Utils/Constants.swift`
2. Find the `apiBaseURL` constant

**For Simulator (default):**
```swift
static let apiBaseURL = "http://localhost:8000"
```

**For Physical Device:**
```swift
// Replace with your Mac's IP address
static let apiBaseURL = "http://192.168.1.XXX:8000"
```

**To find your Mac's IP address:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Look for something like: `inet 192.168.1.123`

---

### Step 4: Select Target Device

In Xcode toolbar, click the device dropdown (next to the scheme/play button).

**Choose:**
- iPhone 15 Pro (simulator) - for development
- Your iPhone (if connected via USB) - for device testing

---

### Step 5: Build and Run

Click the Play button (▶️) or press **⌘ + R**

**First build takes 2-5 minutes** as Xcode:
- Compiles Swift code
- Links frameworks
- Prepares simulator/device

**What you should see:**
- Build progress in Xcode
- Simulator launches (or app installs on device)
- App opens with tab navigation

---

### Step 6: Verify Backend Connection

**Make sure backend is running first:**
```bash
# In a separate terminal
cd ../../backend
source venv/bin/activate
python main.py
```

**In the iOS app:**
1. Try uploading a document (will fail with stub, but should connect)
2. Check Xcode console for network logs

**If you see connection errors:**
- Check backend is running
- Check `Constants.swift` has correct URL
- For device: Check Mac and iPhone on same WiFi

---

## Common Issues

### Build Errors

**"No signing certificate found"**

**Solution:**
1. Xcode → Settings (⌘ + ,)
2. Accounts tab
3. Add your Apple ID
4. Select the project in navigator
5. Signing & Capabilities tab
6. Select your team

---

**"Could not find or use auto-linked framework"**

**Solution:**
1. Clean build folder: Product → Clean Build Folder (⌘ + Shift + K)
2. Rebuild: ⌘ + B

---

**"Multiple commands produce..."**

**Solution:**
1. File → Project Settings
2. Click "Advanced"
3. Set Build System to "New Build System"

---

### Runtime Errors

**"Failed to connect to API"**

**Checklist:**
1. Is backend server running? 
   - Open http://localhost:8000 in browser
   - Should see JSON response
2. Is `Constants.swift` correct?
   - Simulator: use `localhost`
   - Device: use Mac's IP (192.168.x.x)
3. Same WiFi network? (for device)

---

**"Microphone permission denied"**

**Solution:**
1. Device: Settings → Privacy & Security → Microphone → AIPodcast → ON
2. Simulator: In simulator, click I/O → Input → Internal Microphone

---

**Simulator won't launch**

**Solution:**
1. Xcode → Window → Devices and Simulators
2. Right-click simulator → Delete
3. Create new simulator
4. Try again

---

### Code Issues

**Red errors everywhere**

**Solution:**
1. Xcode might still be indexing - wait 2 minutes
2. Product → Clean Build Folder
3. Restart Xcode

---

**"Cannot find 'X' in scope"**

**Solution:**
- Make sure file is added to target
- Right-click file → Show File Inspector
- Check "Target Membership" includes AIPodcast

---

## Development Workflow

### Daily Workflow
```bash
# 1. Navigate to iOS directory
cd frontend/AIPodcast

# 2. Open Xcode
open AIPodcast.xcodeproj

# 3. Select device/simulator
# 4. Press ⌘+R to run

# Keep backend running in separate terminal
```

### Making Changes

1. Edit Swift files in Xcode
2. Save (⌘+S)
3. Build automatically rebuilds
4. Or manually rebuild: ⌘+B

### Using SwiftUI Previews

Many views have preview code at the bottom:
```swift
#Preview {
    DocumentUploadView()
}
```

Click "Resume" in preview canvas to see live preview without running app.

---

## Understanding the Project

### File Organization

**App Entry Point:**
- `AIPodcastApp.swift` - Defines the app and initial view

**Main View:**
- `ContentView.swift` - Tab navigation

**Feature Views:**
- Each feature (Upload, Player, Question) has its own view
- Keep views small and focused

**ViewModels:**
- Handle business logic and state
- Marked with `@Observable` or `ObservableObject`
- Views observe and react to changes

**Services:**
- Reusable components
- `APIClient` - Network calls
- `AudioPlayer` - Audio playback
- `SpeechRecognizer` - Voice input

### Key Concepts

**@State vs @Binding:**
- `@State` - View owns the data
- `@Binding` - View receives data from parent

**@Observable:**
- Makes a class observable by views
- When properties change, views update automatically

**async/await:**
- Modern Swift concurrency
- Use `await` when calling async functions
- Wrap in `Task { ... }` if in non-async context

---

## Tips for Success

✅ **Start with simulator** - Faster iteration than device

✅ **Use SwiftUI previews** - See changes without running app

✅ **Read build errors carefully** - They usually tell you exactly what's wrong

✅ **Clean build if weird errors** - ⌘ + Shift + K

✅ **Restart Xcode if really stuck** - Sometimes it gets confused

✅ **Test on device before demo** - Simulator ≠ real device

✅ **Use breakpoints** - Click line number to add breakpoint for debugging

✅ **Check Xcode console** - Shows print statements and errors

---

## Next Steps

Once app is running:

1. ✅ Check assigned tickets in Linear/Jira
2. ✅ Start with "iOS Setup" labeled tickets
3. ✅ Read through stub files to understand structure
4. ✅ Implement one feature at a time
5. ✅ Test frequently - small changes, frequent builds

---

## Getting Help

### Stuck for 30+ minutes?

**Post in Slack (#proj-four_thirty):**
```
I'm trying to: [what you want to do]
I'm seeing: [error message or unexpected behavior]
I've tried: [what you've already tried]
Screenshot: [if helpful]
```

### Good Resources

- Apple's SwiftUI tutorials (excellent starting point)
- Stack Overflow (search your error message)
- Official Apple documentation
- Ask Jesse

### Questions Worth Asking

✅ "How does MVVM work in SwiftUI?"
✅ "Why use async/await vs completion handlers?"
✅ "How do I debug network requests?"

❌ "It doesn't work" (too vague - what doesn't work?)
❌ "How do I do everything?" (break it down into smaller questions)

---

*This guide is for apprentice engineers. If something is unclear, let Jesse know!*