import themePreset from "@ianlintner/theme/tailwind.config";

/** @type {import('tailwindcss').Config} */
export default {
  presets: [themePreset],
  content: [
    "./flask_app/templates/**/*.{html,jinja,jinja2}",
    "./flask_app/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@ianlintner/theme/dist/**/*.{js,mjs}",
  ],
  theme: {
    extend: {
      maxWidth: {
        "7xl": "80rem",
      },
    },
  },
  plugins: [],
};
