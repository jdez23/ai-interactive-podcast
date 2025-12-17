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
            .background(isEnabled ? Color.appPrimary : Color.appSecondary)
            .cornerRadius(CornerRadius.md)
            .opacity(configuration.isPressed ? 0.8 : 1.0)
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}

// MARK: - Secondary Button Style
struct SecondaryButtonStyle: ButtonStyle {
    var isEnabled: Bool = true
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.appBodyBold)
            .foregroundColor(isEnabled ? Color.appPrimary : Color.appSecondaryText)
            .frame(maxWidth: .infinity)
            .padding(.vertical, Spacing.md)
            .background(Color.appSecondaryBackground)
            .cornerRadius(CornerRadius.md)
            .overlay(
                RoundedRectangle(cornerRadius: CornerRadius.md)
                    .stroke(isEnabled ? Color.appPrimary : Color.appCardBorder, lineWidth: 1.5)
            )
            .opacity(configuration.isPressed ? 0.8 : 1.0)
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}

// MARK: - Icon Button Style
struct IconButtonStyle: ButtonStyle {
    var backgroundColor: Color = Color.appPrimary
    var foregroundColor: Color = .white
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.title3)
            .foregroundColor(foregroundColor)
            .padding(Spacing.md)
            .background(backgroundColor)
            .cornerRadius(CornerRadius.md)
            .opacity(configuration.isPressed ? 0.8 : 1.0)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}

// MARK: - Previews
#Preview("Button Styles - Light Mode") {
    VStack(spacing: Spacing.lg) {
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
        
        HStack(spacing: Spacing.md) {
            Button(action: {}) {
                Image(systemName: "play.fill")
            }
            .buttonStyle(IconButtonStyle())
            
            Button(action: {}) {
                Image(systemName: "heart.fill")
            }
            .buttonStyle(IconButtonStyle(backgroundColor: .appError))
            
            Button(action: {}) {
                Image(systemName: "square.and.arrow.up")
            }
            .buttonStyle(IconButtonStyle(backgroundColor: .appSecondary))
        }
    }
    .padding()
}

#Preview("Button Styles - Dark Mode") {
    VStack(spacing: Spacing.lg) {
        Button("Primary Button") {}
            .buttonStyle(PrimaryButtonStyle())
        
        Button("Secondary Button") {}
            .buttonStyle(SecondaryButtonStyle())
        
        HStack(spacing: Spacing.md) {
            Button(action: {}) {
                Image(systemName: "play.fill")
            }
            .buttonStyle(IconButtonStyle())
            
            Button(action: {}) {
                Image(systemName: "heart.fill")
            }
            .buttonStyle(IconButtonStyle(backgroundColor: .appError))
        }
    }
    .padding()
    .preferredColorScheme(.dark)
}
