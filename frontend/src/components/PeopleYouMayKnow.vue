<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-md" v-if="users && users.length > 0">
        <h3 class="mb-6 text-xl">People you may know</h3>

        <div class="space-y-4">
            <div class="flex items-center justify-between" v-for="user in users" v-bind:key="user.id">
                <div class="flex items-center space-x-2">
                    <img :src="user.avatar_link" class="w-[40px] rounded-full">

                    <p class="text-xs"><strong>{{ user.name }}</strong></p>
                </div>

                <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }"
                    class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</RouterLink>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import axios from 'axios';
import { User } from '../interfaces';

export default {
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