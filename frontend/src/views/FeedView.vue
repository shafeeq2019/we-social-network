<template>
  <PageLayout>
    <PageHeader :eyebrow="greeting" title="Your feed" />

    <FeedForm :user="null" :posts="posts" />

    <PeopleYouMayKnow variant="strip" />

    <div v-if="loading && posts.length === 0" class="space-y-4" aria-busy="true" aria-label="Loading posts">
      <PostSkeleton v-for="n in 3" :key="n" />
    </div>

    <EmptyState v-else-if="error && posts.length === 0" :icon="WifiOff" title="Couldn't load your feed"
                description="Check your connection and try again.">
      <btn variant="outline" @click="retry">Try again</btn>
    </EmptyState>

    <div v-else-if="posts.length > 0" class="space-y-4">
      <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost" />
    </div>

    <EmptyState v-else :icon="Sparkles" title="Your feed is quiet"
                description="Share your first post or find friends to see what they're up to.">
      <RouterLink :to="{ name: 'search' }"
                  class="inline-flex h-10 items-center gap-2 rounded-full bg-foreground px-5 text-sm font-semibold text-background transition hover:bg-foreground/85">
        <Search class="h-4 w-4" aria-hidden="true" /> Find people
      </RouterLink>
    </EmptyState>

    <div v-if="loadingMore" class="flex justify-center py-6" role="status">
      <Loader2 class="h-5 w-5 animate-spin text-muted-foreground" aria-hidden="true" />
      <span class="sr-only">Loading more posts</span>
    </div>
  </PageLayout>
</template>

<script lang="ts">
import {
  defineComponent
} from 'vue';
import axios from 'axios';
import { Loader2, Search, Sparkles, WifiOff } from 'lucide-vue-next';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import FeedItem from '../components/FeedItem.vue';
import FeedForm from '@/components/FeedForm.vue';
import PostSkeleton from '@/components/PostSkeleton.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import btn from '@/components/ui/Button.vue';
import { useInfiniteScroll } from '@/lib/infiniteScroll';
import { useUserStore } from '@/stores/user';
import {
  Post
} from '../interfaces.ts';

export default defineComponent({
  components: {
    PeopleYouMayKnow,
    FeedItem,
    FeedForm,
    PostSkeleton,
    PageLayout,
    PageHeader,
    EmptyState,
    btn,
    Loader2,
    Search,
  },
  setup() {
    const userStore = useUserStore();
    return { userStore, Sparkles, WifiOff };
  },
  data() {
    return {
      posts: [] as Post[],
      currentPage: 1,
      hasNext: true,
      loading: true,
      loadingMore: false,
      error: false
    };
  },
  computed: {
    greeting(): string {
      const hour = new Date().getHours();
      const part = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
      const firstName = (this.userStore.user.name || '').split(' ')[0];
      return firstName ? `${part}, ${firstName}` : part;
    }
  },
  methods: {
    async getFeeds() {
      this.error = false;
      await axios.get(`/api/post/?page=${this.currentPage}`).then(response => {
        this.hasNext = !!response.data.next;
        this.posts = [...this.posts, ...response.data.results];
      }).catch(error => {
        this.error = true;
        console.log(error);
      }).finally(() => {
        this.loading = false;
        this.loadingMore = false;
      });
    },
    retry() {
      this.loading = true;
      this.getFeeds();
    },
    deletePost(postId: string) {
      this.posts = this.posts.filter(
        post => post.id != postId
      );
    }
  },
  mounted() {
    this.getFeeds();
    useInfiniteScroll(() => {
      if (this.hasNext && !this.loading && !this.loadingMore) {
        this.currentPage += 1;
        this.loadingMore = true;
        this.getFeeds();
      }
    });
  }
});
</script>
