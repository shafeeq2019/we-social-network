<template>
  <section class="surface p-5" aria-labelledby="trends-title">
    <div class="mb-3 flex items-center justify-between">
      <h2 id="trends-title" class="text-base font-bold">Trending now</h2>
      <TrendingUp class="h-4 w-4 text-muted-foreground" aria-hidden="true" />
    </div>

    <ul v-if="loading" class="space-y-4 py-1" aria-hidden="true">
      <li v-for="n in 4" :key="n" class="space-y-2">
        <div class="skeleton h-3.5 w-28" />
        <div class="skeleton h-3 w-14" />
      </li>
    </ul>

    <ol v-else-if="trends.length > 0" class="-mx-2">
      <li v-for="(trend, index) in trends" :key="trend.id ?? index">
        <RouterLink :to="{ name: 'trendsview', params: { hashtag: trend.hashtag } }"
                    class="group flex items-center gap-3 rounded-2xl px-2 py-2.5 transition-colors hover:bg-muted">
          <span class="w-5 text-center font-display text-sm font-bold text-muted-foreground/70">{{ index + 1 }}</span>
          <span class="min-w-0 flex-1">
            <span class="block truncate text-sm font-semibold group-hover:text-primary-soft-foreground dark:group-hover:text-primary">#{{ trend.hashtag }}</span>
            <span class="block text-xs text-muted-foreground">{{ trend.occurences }} {{ trend.occurences === 1 ? 'post' : 'posts' }}</span>
          </span>
          <ArrowUpRight class="h-4 w-4 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" aria-hidden="true" />
        </RouterLink>
      </li>
    </ol>

    <p v-else-if="error" class="py-2 text-sm text-muted-foreground">
      Trends couldn't be loaded.
      <button type="button" class="font-semibold text-foreground underline-offset-2 hover:underline" @click="getTrends">Try again</button>
    </p>

    <div v-else class="flex items-center gap-3 rounded-2xl bg-muted/60 p-3 text-sm text-muted-foreground">
      <Hash class="h-5 w-5 shrink-0" aria-hidden="true" />
      No trending hashtags in the last 24 hours. Start one!
    </div>
  </section>
</template>

<script lang="ts">
/**
 TODO:
  - update the posts count when adding a new post to a trend
*/
import { defineComponent } from 'vue';
import { ArrowUpRight, Hash, TrendingUp } from 'lucide-vue-next';
import { Trend } from '../interfaces';
import axios from 'axios';

export default defineComponent({
  components: { ArrowUpRight, Hash, TrendingUp },
  data() {
    return {
      trends: [] as Trend[],
      loading: true,
      error: false
    };
  },
  methods: {
    getTrends() {
      this.loading = true;
      this.error = false;
      axios.get('/api/post/trends/')
        .then(response => {
          this.trends = response.data;
        }).catch(error => {
          this.error = true;
          console.log(error);
        }).finally(() => {
          this.loading = false;
        });
    }
  },
  created() {
    this.getTrends();
  }
});
</script>
