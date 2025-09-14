/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./pages/**/*.{js,ts,jsx,tsx}",
      "./components/**/*.{js,ts,jsx,tsx}",
      "./app/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          tuc: {
            green: "#008D36",      // TU Chemnitz primary green
            lightgreen: "#8DC63F", // lighter accent
            gray: "#4D4D4D",       // TU Chemnitz dark gray
          },
        },
      },
    },
    plugins: [],
  };
  