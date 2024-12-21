<template>
  <div class="p-4 bg-foreground text-primary border border-border rounded-lg shadow-md" v-if="users && users.length > 0">
    <h3 class="mb-6 text-xl">People you may know</h3>

    <div class="space-y-4">
      <div class="flex items-center justify-between" v-for="user in users" v-bind:key="user.id">
        <div class="flex items-center space-x-2">
          <img :src="user.avatar_link" class="w-[40px] rounded-full">

          <p class="text-xs"><strong>{{ user.name }}</strong></p>
        </div>
        <router-link :to="{ name: 'profile', params: { 'id': user.id } }" v-slot="{ navigate }">
          <btn @click="navigate" role="link" class="px-2 py-1">
            Show
          </btn>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { User } from '../interfaces';
import btn from '@/components/ui/Button.vue';

export default {
  components: { btn },
  data() {
    return {
      users: [] as User[]
    };
  },
  mounted() {
    this.getFriendSuggestions();
  },
  methods: {
    getFriendSuggestions() {
      axios
        .get('/api/friends/suggested/')
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          console.log('error', error);
        });
    }
  }
};
</script>
