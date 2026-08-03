import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0a0a0a',
        surface: '#0e0e10',
        'surface-2': '#111114',
        text: '#f5f5f5',
        muted: '#c8c8c8',
        accent: '#e11d2e',
        'accent-hover': '#c11224',
        border: '#1a1a1a',
        'soft-border': '#1f1f22',
      },
      boxShadow: {
        card: '0 10px 30px rgba(0,0,0,.45)',
        btn: '0 8px 20px rgba(225,29,46,.28)',
      },
    },
  },
  plugins: [],
};

export default config;
