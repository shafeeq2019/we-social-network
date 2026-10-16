import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getCurrentThem(): string {
  if (localStorage.getItem('we.theme') === 'dark' || (!('we.theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
    return 'dark';
  } else {
    document.documentElement.classList.remove('dark');
    return 'light';
  }
}

export function toggleTheme(): string {
  const next = getCurrentThem() === 'dark' ? 'light' : 'dark';
  localStorage.setItem('we.theme', next);
  return getCurrentThem();
}

/**
 * Django's `timesince` returns e.g. "2\u00a0hours, 5\u00a0minutes".
 * Keep only the most significant unit for a calmer UI.
 */
export function formatAgo(value?: string): string {
  if (!value) {
    return '';
  }
  const first = value.replace(/\u00a0/g, ' ').split(',')[0].trim();
  if (/^0\s+minutes?$/.test(first)) {
    return 'Just now';
  }
  return `${first} ago`;
}

const escapeHTML = (text: string) => text
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;');

/**
 * Escapes user text, then turns URLs into external links and #hashtags into
 * in-app links (handled by the router via the data-hashtag attribute).
 */
export function renderRichText(text: string): string {
  return escapeHTML(text || '').replace(
    /(https?:\/\/[^\s<]+[^\s<.,;:!?)])|\B#(\w+)/g,
    (match, url: string | undefined, tag: string | undefined) => {
      if (url) {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer nofollow">${url}</a>`;
      }
      return `<a href="/trends/${tag}" data-hashtag="${tag}">#${tag}</a>`;
    }
  );
}

export function initials(name?: string): string {
  if (!name) {
    return '?';
  }
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part[0]!.toUpperCase())
    .join('');
}
