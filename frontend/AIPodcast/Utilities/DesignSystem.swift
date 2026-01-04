import SwiftUI

// MARK: Colors
extension Color {
    static let appPrimary = Color.blue
    static let appSecondary = Color.gray
    static let appAccent = Color.purple
    
    static let appBackground = Color(.systemBackground)
    static let appSecondaryBackground = Color(.secondarySystemBackground)
    static let appTertiaryBackground = Color(.tertiarySystemBackground)
    
    static let appText = Color.primary
    static let appSecondaryText = Color.secondary
    static let appTertiaryText = Color.secondary.opacity(0.7)
    
    static let appSuccess = Color.green
    static let appWarning = Color.orange
    static let appError = Color.red
    
    static let appCardBackground = Color(.secondarySystemBackground)
    static let appCardBorder = appSeparator
    
    // Adaptive separator that subtly changes between light and dark modes
    static var appSeparator: Color {
        Color(UIColor { trait in
            if trait.userInterfaceStyle == .dark {
                return UIColor.white.withAlphaComponent(0.12)
            } else {
                return UIColor.black.withAlphaComponent(0.15)
            }
        })
    }
}

// MARK: Typography
extension Font {
    //Titles
    static let appLargeTitle = Font.system(size: 34, weight: .bold)
    static let appTitle = Font.system(size: 28, weight: .bold)
    static let appTitle2 = Font.system(size: 22, weight: .bold)
    static let appTitle3 = Font.system(size: 20, weight: .bold)
    
    // Body
    static let appBody = Font.system(size: 17, weight: .regular)
    static let appBodyBold = Font.system(size: 17, weight: .semibold)
    static let appCallout = Font.system(size: 16, weight: .regular)
    
    // Secondary
    static let appSubheadline = Font.system(size: 15, weight: .regular)
    static let appFootnote = Font.system(size: 13, weight: .regular)
    static let appCaption = Font.system(size: 12, weight: .regular)
    static let appCaption2 = Font.system(size: 11, weight: .regular)
}

// MARK: Spacing
enum Spacing {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 48
}

// MARK: Corner Radius
enum CornerRadius {
    static let sm: CGFloat = 8
    static let md: CGFloat = 12
    static let lg: CGFloat = 16
    static let xl: CGFloat = 20
}

// MARK: Shadow
extension View {
    func appCardShadow() -> some View {
        self.shadow(color: Color.black.opacity(0.1), radius: 8, x: 0, y: 2)
    }
    
    func appLightShadow() -> some View {
        self.shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
    }
}

