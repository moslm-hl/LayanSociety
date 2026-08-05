/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        pink: {
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
        },
        marine: {
          700: '#004080',
          800: '#003366',
          900: '#002244',
        },
      },
    },
  },
  plugins: [],
}
