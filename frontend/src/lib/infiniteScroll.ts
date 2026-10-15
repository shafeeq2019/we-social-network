import { onBeforeUnmount } from 'vue';

/**
 * Calls `onReachEnd` when the window is scrolled close to the bottom.
 * Must be called during setup/mounted of a component; the listener is
 * removed automatically when the component unmounts.
 */
export function useInfiniteScroll(onReachEnd: () => void, offset = 400) {
  let ticking = false;

  const check = () => {
    ticking = false;
    const scrolled = window.scrollY + window.innerHeight;
    if (scrolled >= document.documentElement.scrollHeight - offset) {
      onReachEnd();
    }
  };

  const onScroll = () => {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(check);
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onBeforeUnmount(() => window.removeEventListener('scroll', onScroll));
}
