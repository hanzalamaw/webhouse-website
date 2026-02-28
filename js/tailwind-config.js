/**
 * Tailwind CSS Configuration
 * Custom theme configuration for WebHouse Inc.
 */
if (typeof tailwind !== 'undefined') {
    tailwind.config = {
        darkMode: false,
        theme: {
            extend: {
                colors: {
                    "primary": "#b90606",
                    "primary-hover": "#c80505",
                    "primary-light": "#c80505",
                    "primary-soft": "#ffe4e6",
                    "background-light": "#ffffff",
                    "background-alt": "#f8f9fa",
                    "background-dark": "#111111",
                    "surface-dark": "#1c1917",
                    "surface-light": "#f3f4f6",
                },
                fontFamily: {
                    "display": ["Plus Jakarta Sans", "sans-serif"],
                    "sans": ["Inter", "sans-serif"],
                },
                borderRadius: {
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "1rem",
                    "2xl": "1.5rem",
                    "3xl": "2rem",
                    "4xl": "2.5rem",
                    "full": "9999px"
                },
                boxShadow: {
                    "glow": "0 0 30px -5px rgba(185, 6, 6, 0.4)",
                    "glow-strong": "0 0 50px -10px rgba(200, 5, 5, 0.6)",
                    "card": "0 20px 40px -15px rgba(0, 0, 0, 0.1)",
                },
                backgroundImage: {
                    'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                }
            },
        },
    };
}

