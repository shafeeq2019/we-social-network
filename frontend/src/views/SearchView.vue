<template lang="">
  <div
    class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-4 xl:grid-cols-4 gap-4 text-primary">
    <div class="main-center col-span-1 lg:col-span-3 space-y-4">
      <div class="bg-background border border-border rounded-lg">
        <form class="p-4 flex space-x-4" @submit.prevent="submitForm">
          <input type="search" class="p-4 w-full bg-foreground rounded-lg" v-model="query"
                 placeholder="What are you looking for?">
          <btn class="px-4" type="submit">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
            </svg>
          </btn>
        </form>
      </div>
      <div v-if="users.length > 0"
           class="bg-foreground border border-border rounded-lg p-4 grid grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-4 gap-4">
        <router-link :to="{ name: 'profile', params: { 'id': user.id } }" v-for="(user, index) in users" :key="index">
          <div class="p-4 text-center bg-primary rounded-lg hover:bg-primary-hover">
            <img :src="user.avatar_link" class="mb-6 mx-auto w-12 h-12 rounded-full object-cover object-center">
            <p class="break-all"><strong>{{user.name}}</strong></p>
            <div class="mt-6 flex space-x-4 justify-around">
              <p class="text-xs text-secondary">{{user.friends_count}} friends</p>
              <p class="text-xs text-secondary">{{user.posts_count}} posts</p>
            </div>
          </div>
        </router-link>
      </div>
      <FeedItem v-for="(post, index) in posts" :key="index" :post="post" />
    </div>
    <!-- People you may know -->
    <div class="main-right col-span-1 lg:col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue';
import btn from '../components/ui/Button.vue';

export default defineComponent({
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    btn
  },
  data() {
    return {
      query: '',
      users: [],
      posts: []
    };
  },
  methods: {
    submitForm() {
      axios.post('api/search/', {
        query: this.query
      }).then(response => {
        this.users = response.data.users;
        this.posts = response.data.posts;
      }).catch(e => {
        console.log("error", e);
      });
    }
  }
});
</script>

<style lang="">

</style>
