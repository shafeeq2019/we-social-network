import { defineStore } from 'pinia';

let hideTimer: ReturnType<typeof setTimeout> | undefined;

export const useToastStore = defineStore({
  id: 'toast',

  state: () => ({
    ms: 0,
    message: '',
    classes: '',
    isVisible: false
  }),

  getters: {
    // Callers pass a Tailwind colour class (e.g. "bg-red-300") as a hint;
    // the toast itself is styled by variant.
    variant: (state): 'success' | 'error' => (/red|destructive|error/.test(state.classes) ? 'error' : 'success')
  },

  actions: {
    showToast(ms: number, message: string, classes: string) {
      this.ms = ms;
      this.message = message;
      this.classes = classes;
      this.isVisible = true;

      clearTimeout(hideTimer);
      hideTimer = setTimeout(() => {
        this.isVisible = false;
      }, this.ms);
    },

    hide() {
      clearTimeout(hideTimer);
      this.isVisible = false;
    }
  }
});
