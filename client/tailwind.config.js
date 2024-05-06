import daisyui from 'daisyui';

export default {
  mode: 'jit',
  purge: ['./index.html', './src/**/*.{svelte,js,ts}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        Unbutton: ['Unbutton'],
        Comikan: ['Comikan'],
        Buba: ['Buba'],
        BadComic: ['BadComic'],
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["light", "dark", "lemonade"],
  },
}

