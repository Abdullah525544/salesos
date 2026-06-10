/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#4F46E5', 50: '#EEF2FF', 100: '#E0E7FF', 200: '#C7D2FE', 300: '#A5B4FC', 400: '#818CF8', 500: '#4F46E5', 600: '#4338CA', 700: '#3730A3', 800: '#312E81', 900: '#1E1B4B' },
        surface: { DEFAULT: '#111827', light: '#1F2937', lighter: '#374151' },
        bg: { DEFAULT: '#0B1220', card: '#111827' },
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
      backdropBlur: { xs: '2px' },
    },
  },
  plugins: [],
};
