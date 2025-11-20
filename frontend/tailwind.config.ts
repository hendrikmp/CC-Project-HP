import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#111111",
        surface: "#151515",
        "surface-highlight": "#1B1B1B",
        primary: "#00C96B",
        "primary-dark": "#00A859",
        secondary: "#FF7A1A",
        "secondary-dark": "#E66300",
        text: "#EDEDED",
        "text-muted": "#A1A1A1",
      },
      fontFamily: {
        sans: ['var(--font-inter)'],
      },
    },
  },
  plugins: [],
};
export default config;
