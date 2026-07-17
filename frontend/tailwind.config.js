/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          950: '#050811',
          900: '#0a0f1e',
          800: '#111827',
          700: '#1f2937',
        }
      }
    },
  },
  plugins: [],
}
