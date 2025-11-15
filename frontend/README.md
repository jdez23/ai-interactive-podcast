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
cd frontend/AIPodcast

# Open in Xcode
open AIPodcast.xcodeproj

# Or from command line
xed .
```

## Project Structure
```
AIPodcast/
├── AIPodcastApp.swift       # App entry point
├── ContentView.swift         # Main view with tab navigation
├── Views/                    # UI components organized by feature
│   ├── Upload/
│   │   └── DocumentUploadView.swift
│   ├── Player/
│   │   ├── PodcastPlayerView.swift
│   │   └── AudioWaveformView.swift
│   └── Question/
│       └── QuestionInputView.swift
├── ViewModels/               # Observable objects for state management
│   ├── DocumentUploadViewModel.swift
│   ├── PodcastPlayerViewModel.swift
│   └── QuestionViewModel.swift
├── Models/                   # Data models matching API responses
│   ├── Document.swift
│   ├── Podcast.swift
│   └── Question.swift
├── Services/                 # Networking, audio, speech
│   ├── APIClient.swift
│   ├── AudioPlayer.swift
│   └── SpeechRecognizer.swift
└── Utils/                    # Helper functions
    ├── Constants.swift
    └── Extensions.swift
```

## Architecture

This app uses **MVVM** (Model-View-ViewModel) architecture:

- **Views** - SwiftUI views that display UI
- **ViewModels** - ObservableObjects that manage state and business logic
- **Models** - Data structures matching API responses
- **Services** - Reusable components (networking, audio, etc.)
```
┌─────────┐     ┌──────────────┐     ┌──────────┐     ┌─────────┐
│  View   │────▶│  ViewModel   │────▶│ Service  │────▶│   API   │
└─────────┘     └──────────────┘     └──────────┘     └─────────┘
     │                  │
     │                  ▼
     └──────────── @Published State
```

## Key Features

### Document Upload
- Select PDFs from Files app
- Upload to backend API
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

**For testing on physical device:**
1. Find your Mac's local IP: `ifconfig | grep inet`
2. Update `Utils/Constants.swift` with your Mac's IP
3. Ensure Mac and iPhone on same WiFi network

## Common Issues

**"Failed to connect to API"**
- Check backend server is running: `cd ../../backend && python main.py`
- Check API base URL in `Utils/Constants.swift`
- For physical device: Use Mac's IP address, not `localhost`

**"Microphone permission denied"**
- Settings → Privacy & Security → Microphone
- Enable for AIPodcast app

**Audio not playing**
- Check device is not in silent mode
- Check volume is up
- Try simulator first to isolate device issues

## Development

### Running the App

1. Open `AIPodcast.xcodeproj` in Xcode
2. Select target device/simulator
3. Press ⌘+R to build and run

### Running Tests

- Press ⌘+U to run all tests
- Or ⌘+6 to open test navigator

### Code Style

- Follow [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- Use descriptive variable names
- Comment complex logic
- Keep views small and focused

## Resources

- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [AVFoundation Guide](https://developer.apple.com/documentation/avfoundation)
- [Speech Framework](https://developer.apple.com/documentation/speech)
- [Async/Await in Swift](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html)

## Need Help?

1. Check [SETUP.md](SETUP.md) for setup issues
2. Check [API_SPEC.md](../../docs/API_SPEC.md) for API details
3. Post in Slack group chat