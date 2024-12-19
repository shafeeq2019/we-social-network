<template>
  <div class="p-4 bg-foreground text-primary border border-border rounded-lg shadow-md" v-if="!loading">
    <h3 class="mb-6 text-xl">Trends</h3>
    <div class="space-y-4" v-if="trends && trends.length > 0">
      <div class="flex items-center justify-between" v-for="(trend, index) in trends" :key="index">
        <p class="text-xs">
          <strong>#{{ trend.hashtag }}</strong><br>
          <span class="text-secondary">{{ trend.occurences }} posts</span>
        </p>
        <router-link :to="{ name: 'trendsview', params: { 'hashtag': trend.hashtag } }"
                     class="py-2 px-3 bg-button-primary text-white text-xs rounded-lg">Explore</router-link>
      </div>
    </div>
    <div v-else class="flex items-center justify-center">
      <p class="pr-2 md:text-sm text-secondary font-medium">There are no new trends in the last 24 hours</p>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
           class="w-9 h-9 text-secondary">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M5.25 8.25h15m-16.5 7.5h15m-1.8-13.5-3.9 19.5m-2.1-19.5-3.9 19.5" />
      </svg>
    </div>
  </div>
</template>
<script  lang="ts">
/**
 TODO:
  - update the posts count when adding a new post to a trend
*/
import { defineComponent } from 'vue';
import { Trend } from '../interfaces';
import axios from 'axios';

export default defineComponent({
  data() {
    return {
      trends: [] as Trend[],
      loading: true
    };
  },
  methods: {
    getTrends() {
      axios.get('/api/post/trends/')
        .then(response => {
          this.trends = response.data;
          this.loading = false;
        }).catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.getTrends();
  }
});
</script>
