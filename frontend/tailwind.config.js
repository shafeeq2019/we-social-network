import animate from 'tailwindcss-animate';
import defaultTheme from 'tailwindcss/defaultTheme';

/** @type {import('tailwindcss').Config} */
export const darkMode = ['class'];
export const safelist = ['dark'];
export const content = [
  './index.html',
  './src/**/*.{ts,tsx,vue}',
];
export const theme = {
  container: {
    center: true,
    padding: '2rem',
    screens: {
      '2xl': '1400px',
    },
  },
  extend: {
    fontFamily: {
      sans: ['Figtree', ...defaultTheme.fontFamily.sans],
      display: ['"Bricolage Grotesque"', 'Figtree', ...defaultTheme.fontFamily.sans],
    },
    colors: {
      border: 'hsl(var(--border))',
      input: 'hsl(var(--input))',
      ring: 'hsl(var(--ring))',
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      primary: {
        DEFAULT: 'hsl(var(--primary))',
        foreground: 'hsl(var(--primary-foreground))',
        soft: 'hsl(var(--primary-soft))',
        'soft-foreground': 'hsl(var(--primary-soft-foreground))',
      },
      secondary: {
        DEFAULT: 'hsl(var(--secondary))',
        foreground: 'hsl(var(--secondary-foreground))',
      },
      destructive: {
        DEFAULT: 'hsl(var(--destructive))',
        foreground: 'hsl(var(--destructive-foreground))',
      },
      muted: {
        DEFAULT: 'hsl(var(--muted))',
        foreground: 'hsl(var(--muted-foreground))',
      },
      accent: {
        DEFAULT: 'hsl(var(--accent))',
        foreground: 'hsl(var(--accent-foreground))',
      },
      popover: {
        DEFAULT: 'hsl(var(--popover))',
        foreground: 'hsl(var(--popover-foreground))',
      },
      card: {
        DEFAULT: 'hsl(var(--card))',
        foreground: 'hsl(var(--card-foreground))',
      },
      like: 'hsl(var(--like))',
      success: 'hsl(var(--success))',
    },
    borderRadius: {
      '4xl': '2rem',
      lg: 'var(--radius)',
      md: 'calc(var(--radius) - 4px)',
      sm: 'calc(var(--radius) - 8px)',
    },
    boxShadow: {
      soft: '0 1px 2px hsl(var(--shadow-color) / 0.04), 0 2px 8px -2px hsl(var(--shadow-color) / 0.05)',
      lift: '0 2px 4px hsl(var(--shadow-color) / 0.04), 0 12px 32px -8px hsl(var(--shadow-color) / 0.14)',
      glow: '0 6px 20px -6px hsl(var(--primary) / 0.55)',
    },
    keyframes: {
      'accordion-down': {
        from: { height: 0 },
        to: { height: 'var(--radix-accordion-content-height)' },
      },
      'accordion-up': {
        from: { height: 'var(--radix-accordion-content-height)' },
        to: { height: 0 },
      },
      'collapsible-down': {
        from: { height: 0 },
        to: { height: 'var(--radix-collapsible-content-height)' },
      },
      'collapsible-up': {
        from: { height: 'var(--radix-collapsible-content-height)' },
        to: { height: 0 },
      },
      'fade-up': {
        from: { opacity: 0, transform: 'translateY(8px)' },
        to: { opacity: 1, transform: 'translateY(0)' },
      },
      pop: {
        '0%': { transform: 'scale(1)' },
        '40%': { transform: 'scale(1.3)' },
        '100%': { transform: 'scale(1)' },
      },
    },
    animation: {
      'accordion-down': 'accordion-down 0.2s ease-out',
      'accordion-up': 'accordion-up 0.2s ease-out',
      'collapsible-down': 'collapsible-down 0.2s ease-in-out',
      'collapsible-up': 'collapsible-up 0.2s ease-in-out',
      'fade-up': 'fade-up 0.35s cubic-bezier(0.22, 1, 0.36, 1) both',
      pop: 'pop 0.35s cubic-bezier(0.22, 1, 0.36, 1)',
    },
  },
};
export const plugins = [animate];
