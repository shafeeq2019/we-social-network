import { defineStore } from 'pinia';
import axios from 'axios';

// Holds the unread notification count shown as a badge in the navigation.
export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    unread: 0
  }),

  actions: {
    async fetchUnread() {
      try {
        const response = await axios.get('/api/notification/');
        this.unread = response.data.count ?? response.data.results?.length ?? 0;
      } catch (error) {
        console.log(error);
      }
    },

    markOneRead() {
      this.unread = Math.max(0, this.unread - 1);
    }
  }
});
