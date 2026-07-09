// tailwind.config.js
// Defines our dark-blue banking theme colors, used everywhere via classes
// like "bg-navy-900" or "text-accent-500"

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#050b18",   // deepest background
          900: "#0a1428",   // main page background
          800: "#101c34",   // card background
          700: "#182a4a",   // hover / border
          600: "#22406e",
        },
        accent: {
          500: "#3b82f6",   // primary blue (buttons, links)
          600: "#2563eb",
        },
        risk: {
          safe: "#22c55e",     // green
          medium: "#eab308",   // yellow
          high: "#f97316",     // orange
          critical: "#ef4444", // red
        },
      },
    },
  },
  plugins: [],
}