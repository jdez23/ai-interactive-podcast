# AI Interactive Podcast - iOS App

SwiftUI iOS application for the AI Interactive Podcast platform.

## Requirements

- macOS 14.0 or later
- Xcode 15.0 or later
- iOS 17.0+ target device or simulator

## Quick Start

See [SETUP.md](SETUP.md) for detailed setup instructions.
```bash
# From project root
cd ios

# Open in Xcode
open AIPodcast.xcodeproj

# Or from command line
xed .
```

## Project Structure

- **Views/** - SwiftUI views organized by feature
- **ViewModels/** - Observable objects for state management
- **Models/** - Data models matching API responses
- **Services/** - Networking, audio playback, speech recognition
- **Utils/** - Helper functions, extensions, constants

## Architecture

This app uses MVVM (Model-View-ViewModel) architecture:
- **Views** observe **ViewModels**
- **ViewModels** use **Services** to fetch data
- **Services** communicate with backend API
```
┌─────────┐     ┌──────────────┐     ┌──────────┐     ┌─────────┐
│  View   │────▶│  ViewModel   │────▶│ Service  │────▶│   API   │
└─────────┘     └──────────────┘     └──────────┘     └─────────┘
     │                  │
     │                  ▼
     └──────────── ObservableObject
```

## Key Features

### Document Upload
- Select PDFs from Files app
- Upload to backend
- Show processing status

### Podcast Player
- Stream podcast audio from backend
- Display waveform visualization
- Playback controls (play, pause, seek)

### Interactive Q&A
- Tap to interrupt podcast
- Voice or text input for questions
- Play AI-generated answers
- Resume podcast after answer

## API Integration

Backend API runs at: `http://localhost:8000` (development)

For testing on device, you'll need to:
1. Find your Mac's local IP: `ifconfig | grep inet`
2. Update `Constants.swift` with IP address
3. Ensure Mac and iPhone on same WiFi

## Testing

Run tests in Xcode:
- ⌘ + U to run all tests
- ⌘ + 6 to open test navigator

## Common Issues

**"Failed to connect to API"**
- Check backend server is running: `cd ../backend && python main.py`
- Check API base URL in `Constants.swift`
- For device testing, use Mac's IP address not `localhost`

**"Microphone permission denied"**
- Go to Settings → Privacy → Microphone
- Enable for AI Podcast app

**Audio not playing**
- Check device is not in silent mode
- Check volume is up
- Try in simulator first

## Next Steps

1. Review the starter code in each file
2. Check your assigned tickets in Linear
3. Start with tickets labeled "iOS Setup"
4. Ask questions in #apprentice-ai-podcast

## Resources

- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [AVFoundation Guide](https://developer.apple.com/documentation/avfoundation)
- [Speech Framework](https://developer.apple.com/documentation/speech)