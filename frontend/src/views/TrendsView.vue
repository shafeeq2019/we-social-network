<template>
  <PageLayout>
    <header class="surface relative overflow-hidden p-6 sm:p-8">
      <div class="pointer-events-none absolute -right-6 -top-10 select-none font-display text-[180px] font-extrabold leading-none text-primary/10" aria-hidden="true">#</div>
      <p class="eyebrow">Trending topic</p>
      <h1 class="mt-1 break-all text-3xl font-extrabold sm:text-4xl">#{{ hashtag }}</h1>
      <p class="mt-2 text-sm text-muted-foreground">
        <template v-if="!loading">{{ posts.length }}{{ hasNext ? '+' : '' }} {{ posts.length === 1 ? 'post' : 'posts' }} from the community</template>
        <template v-else>Loading posts…</template>
      </p>
    </header>

    <div v-if="loading && posts.length === 0" class="space-y-4">
      <PostSkeleton v-for="n in 2" :key="n" />
    </div>
    <div v-else-if="posts.length > 0" class="space-y-4">
      <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost" />
    </div>
    <EmptyState v-else :icon="Hash" title="Nothing here yet"
                :description="`Be the first to post about #${hashtag}.`" />

    <div v-if="loadingMore" class="flex justify-center py-6" role="status">
      <Loader2 class="h-5 w-5 animate-spin text-muted-foreground" aria-hidden="true" />
      <span class="sr-only">Loading more posts</span>
    </div>
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { Hash, Loader2 } from 'lucide-vue-next';
import FeedItem from '../components/FeedItem.vue';
import PostSkeleton from '@/components/PostSkeleton.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import { useInfiniteScroll } from '@/lib/infiniteScroll';
import { Post } from '../interfaces';

export default defineComponent({
  props: ['hashtag'],
  async beforeRouteUpdate(to) {
    this.posts = [];
    this.currentPage = 1;
    this.loading = true;
    await this.getFeeds(to.params.hashtag);
  },
  components: {
    FeedItem,
    PostSkeleton,
    PageLayout,
    EmptyState,
    Loader2,
  },
  setup() {
    return { Hash };
  },
  data() {
    return {
      posts: [] as Post[],
      currentPage: 1,
      hasNext: true,
      loading: true,
      loadingMore: false
    };
  },
  methods: {
    async getFeeds(hashtag: string | string[]) {
      await axios.get('/api/post/', {
        params: { trend: hashtag, page: this.currentPage }
      }).then(response => {
        this.hasNext = !!response.data.next;
        this.posts = [...this.posts, ...response.data.results];
      }).catch(error => {
        console.log(error);
      }).finally(() => {
        this.loading = false;
        this.loadingMore = false;
      });
    },
    deletePost(postId: string) {
      this.posts = this.posts.filter(
        post => post.id != postId
      );
    }
  },
  mounted() {
    this.getFeeds(this.hashtag);
    useInfiniteScroll(() => {
      if (this.hasNext && !this.loading && !this.loadingMore) {
        this.currentPage += 1;
        this.loadingMore = true;
        this.getFeeds(this.hashtag);
      }
    });
  }
});
</script>
