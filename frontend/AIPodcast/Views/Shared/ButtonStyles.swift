import SwiftUI

// MARK: - Primary Button Style
struct PrimaryButtonStyle: ButtonStyle {
    var isEnabled: Bool = true
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.appBodyBold)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .padding(.vertical, Spacing.md)
            .padding(.horizontal, 20)
            .background(isEnabled ? Color.appPrimary : Color.appSecondary)
            .cornerRadius(CornerRadius.xl)
            .glassEffect(.regular.tint(isEnabled ? Color.appPrimary : Color.appSecondary), in: RoundedRectangle(cornerRadius: 16))
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

// MARK: - Secondary Button Style
struct SecondaryButtonStyle: ButtonStyle {
    var isEnabled: Bool = true
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.appBodyBold)
            .foregroundColor(isEnabled ? Color.white : Color.appSecondaryText)
            .frame(maxWidth: .infinity)
            .padding(.vertical, Spacing.md)
            .padding(.horizontal, 20)
            .glassEffect(.clear, in: RoundedRectangle(cornerRadius: 16))
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

// MARK: - Icon Button Style
struct IconButtonStyle: ButtonStyle {
    enum Style {
        case glass
        case circularAdd(size: CGFloat = 56)
    }
    
    var tintColor: Color = Color.white
    var style: Style = .glass
    
    func makeBody(configuration: Configuration) -> some View {
        Group {
            switch style {
            case .glass:
                configuration.label
                    .font(.title3)
                    .foregroundColor(.white)
                    .padding(Spacing.md)
                    .glassEffect(.clear, in: Circle())
                    .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
                    .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
                
            case .circularAdd(let size):
                ZStack {
                    Circle()
                        .fill(Color.appPrimary)
                        .frame(width: size, height: size)
                    
                    Image(systemName: "plus")
                        .font(.system(size: size * 0.43, weight: .medium))
                        .foregroundColor(.white)
                }
                .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
                .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
            }
        }
    }
}

// MARK: - Bare Icon Button Style
struct BareIconButtonStyle: ButtonStyle {
    enum Size {
        case mini
        case regular
        case large
        
        var fontSize: CGFloat {
            switch self {
            case .mini: return 16
            case .regular: return 20
            case .large: return 24
            }
        }
    }
    
    var tintColor: Color = .white
    var size: Size = .regular
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: size.fontSize, weight: .semibold))
            .foregroundColor(tintColor)
            .opacity(configuration.isPressed ? 0.6 : 1.0)
            .scaleEffect(configuration.isPressed ? 0.9 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

// MARK: - Previews
#Preview("Button Styles - Dark Mode") {
    ZStack {
        LinearGradient(
            colors: [
                Color.blue.opacity(0.2),
                Color.indigo.opacity(0.2),
                Color.black.opacity(0.1)
            ],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
        
        VStack(spacing: Spacing.lg) {
            
// LARGE BUTTONS
            Text("Large Buttons")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.white)
            
            Button("Primary Button") {}
                .buttonStyle(PrimaryButtonStyle())
            
            Button("Primary Disabled") {}
                .buttonStyle(PrimaryButtonStyle(isEnabled: false))
                .disabled(true)
            
            Button("Secondary Button") {}
                .buttonStyle(SecondaryButtonStyle())
            
            Button("Secondary Disabled") {}
                .buttonStyle(SecondaryButtonStyle(isEnabled: false))
                .disabled(true)
            
            Divider()
            
// ICON BUTTTONS
            Text("Icon Buttons")
                .font(.headline)
                .foregroundColor(.white)
            
            HStack(spacing: Spacing.md) {
                Button(action: {}) {
                    Image(systemName: "play.fill")
                }
                .buttonStyle(IconButtonStyle())
                
                Button(action: {}) {
                    Image(systemName: "square.and.arrow.up")
                }
                .buttonStyle(IconButtonStyle())
                
                Button(action: {}) {
                    Image(systemName: "plus")
                }
                .buttonStyle(IconButtonStyle())
            }
            
            Divider()
            
// BARE ICON BUTTONS
            Text("Bare Icon Buttons")
                .font(.headline)
                .foregroundColor(.white)
            
            VStack(spacing: 16) {
                HStack(spacing: 20) {
                    Text("Mini:")
                        .foregroundColor(.white)
                    Button(action: {}) {
                        Image(systemName: "gobackward.15")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .mini))
                    
                    Button(action: {}) {
                        Image(systemName: "goforward.30")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .mini))
                    
                    Button(action: {}) {
                        Image(systemName: "arrow.down")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .mini))
                    
                    Button(action: {}) {
                        Image(systemName: "play.fill")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .mini))
                    
                    Button(action: {}) {
                        Image(systemName: "square.and.arrow.up")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .mini))
                    
                    Button(action: {}) {
                        Image(systemName: "trash.fill")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .mini))
                }
                
                HStack(spacing: 20) {
                    Text("Regular:")
                        .foregroundColor(.white)
                    Button(action: {}) {
                        Image(systemName: "gobackward.15")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .regular))
                    
                    Button(action: {}) {
                        Image(systemName: "goforward.30")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .regular))
                    
                    Button(action: {}) {
                        Image(systemName: "arrow.down")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .regular))
                    
                    Button(action: {}) {
                        Image(systemName: "play.fill")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .regular))
                    
                    Button(action: {}) {
                        Image(systemName: "square.and.arrow.up")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .regular))
                    
                    Button(action: {}) {
                        Image(systemName: "trash.fill")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .regular))
                }
                
                HStack(spacing: 20) {
                    Text("Large:")
                        .foregroundColor(.white)
                    
                    Button(action: {}) {
                        Image(systemName: "gobackward.15")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .large))
                    
                    Button(action: {}) {
                        Image(systemName: "goforward.30")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .large))
                    
                    Button(action: {}) {
                        Image(systemName: "arrow.down")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .large))
                    
                    Button(action: {}) {
                        Image(systemName: "play.fill")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .large))
                    
                    Button(action: {}) {
                        Image(systemName: "square.and.arrow.up")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .large))
                    
                    Button(action: {}) {
                        Image(systemName: "trash.fill")
                    }
                    .buttonStyle(BareIconButtonStyle(size: .large))
                }
            }
        }
        .padding()
        .preferredColorScheme(.light)
    }
}
