<template lang="">
    <div class="max-w-7xl mx-auto grid-cols-4 gap-4 hidden md:grid">
        <div class="main-center col-span-3 space-y-4">
            <FeedForm :user="null" :posts="posts" />
            <div v-if="posts.length > 0" class="space-y-4">
                <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost"
               />
            </div>
            <div v-else-if="!loading" class="bg-white shadow-md sm:rounded-lg p-6">
                <div class="text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                        stroke="currentColor" class="h-36 w-40 text-purple-600 mx-auto ">
                        <path strokeLinecap="round" strokeLinejoin="round"
                            d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
                    </svg>
                    <p class="mt-2 text-xl font-semibold text-gray-700">You don't have any posts yet and no friends
                        either. Create a new post or add friends to see new feeds</p>
                </div>
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>

    <div class="max-w-7xl mx-auto md:hidden space-y-4">
        <FeedForm :user="null" :posts="posts" />
        <PeopleYouMayKnow />
        <Trends />
        <div v-if="posts.length > 0" class="space-y-4">
            <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost"/>
        </div>
        <div v-else-if="!loading" class="bg-white shadow-md sm:rounded-lg p-6">
            <div class="text-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                    stroke="currentColor" class="h-36 w-40 text-purple-600 mx-auto ">
                    <path strokeLinecap="round" strokeLinejoin="round"
                        d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
                </svg>
                <p class="mt-2 text-xl font-semibold text-gray-700">You don't have any posts yet and no friends
                    either. Create a new post or add friends to see new feeds</p>
            </div>
        </div>

    </div>
</template>
<script lang="ts">
import {
  defineComponent
} from 'vue';
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue';
import FeedForm from '@/components/FeedForm.vue';
import {
  Post
} from '../interfaces.ts';
export default defineComponent({
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    FeedForm
  },
  data() {
    return {
      posts: [] as Post[],
      body: '',
      currentPage: 1,
      hasNext: true,
      loading: true
    };
  },
  methods: {
    async getFeeds() {
      await axios.get(`/api/post/?page=${this.currentPage}`).then(response => {
        if (response.data.next) {
          this.hasNext = true;
        }
        this.loading = false;
        this.posts = [...this.posts, ...response.data.results];
      }).catch(error => {
        this.loading = false;
        console.log(error);
      });
    },
    deletePost(postId: string) {
      this.posts = this.posts.filter(
        post => post.id != postId
      );
    }
  },
  mounted() {
    const onScroll = () => {
      const bottomOfWindow = parseInt(`${document.documentElement.scrollTop + window.innerHeight}`) === document.documentElement.offsetHeight;
      if (bottomOfWindow && this.hasNext) {
        this.currentPage += 1;
        this.hasNext = false;
        this.getFeeds();
      }
    };
    this.getFeeds();
    window.onscroll = onScroll;
    window.ontouchmove = onScroll;
  }
});
</script>
<style lang=""></style>