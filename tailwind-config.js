// Shared Tailwind CDN configuration for GoTech Solutions
// Loaded on every page AFTER the Tailwind CDN <script> tag.
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "error-container": "#ffdad6",
        "surface-white": "#FFFFFF",
        "primary-fixed-dim": "#92d4b5",
        "on-secondary": "#ffffff",
        "on-primary": "#ffffff",
        "inverse-on-surface": "#eff1f0",
        "secondary-container": "#ead5ff",
        "outline": "#707973",
        "on-secondary-fixed": "#231534",
        "surface-variant": "#e1e3e2",
        "tertiary-container": "#b1b115",
        "surface-bright": "#f8faf9",
        "on-tertiary-fixed-variant": "#4a4900",
        "background": "#f8faf9",
        "surface": "#f8faf9",
        "tertiary": "#626200",
        "surface-container-high": "#e6e9e8",
        "surface-dim": "#d8dada",
        "on-secondary-fixed-variant": "#504062",
        "surface-container-highest": "#e1e3e2",
        "on-tertiary-container": "#424200",
        "tertiary-fixed": "#eae951",
        "secondary-fixed-dim": "#d3bee8",
        "on-primary-fixed-variant": "#055139",
        "surface-container-low": "#f2f4f3",
        "primary-container": "#09533b",
        "secondary-fixed": "#eedbff",
        "on-error": "#ffffff",
        "inverse-primary": "#92d4b5",
        "on-primary-container": "#84c5a6",
        "error": "#ba1a1a",
        "on-tertiary-fixed": "#1d1d00",
        "on-error-container": "#93000a",
        "on-background": "#191c1c",
        "inverse-surface": "#2e3131",
        "surface-container-lowest": "#ffffff",
        "tertiary-fixed-dim": "#cdcc36",
        "border-light": "#E4E9EA",
        "on-surface": "#191c1c",
        "on-surface-variant": "#404943",
        "ink": "#000000",
        "primary-fixed": "#aef1d0",
        "secondary": "#68577b",
        "on-secondary-container": "#6b5a7e",
        "primary": "#003a28",
        "on-primary-fixed": "#002115",
        "surface-container": "#eceeed",
        "outline-variant": "#bfc9c2",
        "on-tertiary": "#ffffff",
        "surface-tint": "#286a50",
        "soft-blue": "#C9D3F3",
        "lavender": "#DEC9F3",
        "pale-yellow": "#EBEA52"
      },
      borderRadius: {
        DEFAULT: "0.125rem",
        lg: "0.25rem",
        xl: "0.5rem",
        full: "0.75rem"
      },
      spacing: {
        gutter: "24px",
        "section-v-padding-mobile": "60px",
        "section-v-padding": "100px",
        unit: "4px",
        "container-max": "1140px"
      },
      fontFamily: {
        "label-caps": ["Hanken Grotesk"],
        "display-lg-mobile": ["Libre Caslon Text"],
        "headline-md": ["Libre Caslon Text"],
        "body-main": ["Hanken Grotesk"],
        "display-lg": ["Libre Caslon Text"],
        "stat-number": ["Libre Caslon Text"],
        "lead-paragraph": ["Hanken Grotesk"]
      },
      fontSize: {
        "label-caps": ["12px", { lineHeight: "1", letterSpacing: "0.1em", fontWeight: "700" }],
        "display-lg-mobile": ["36px", { lineHeight: "1.2", fontWeight: "700" }],
        "headline-md": ["32px", { lineHeight: "1.2", fontWeight: "600" }],
        "body-main": ["16px", { lineHeight: "1.65", fontWeight: "400" }],
        "display-lg": ["56px", { lineHeight: "1.1", fontWeight: "700" }],
        "stat-number": ["48px", { lineHeight: "1", fontWeight: "700" }],
        "lead-paragraph": ["20px", { lineHeight: "1.6", fontWeight: "400" }]
      }
    }
  }
};
