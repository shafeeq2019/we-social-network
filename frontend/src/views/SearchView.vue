<template>
  <PageLayout>
    <PageHeader title="Explore" description="Find people and conversations across We." />

    <form role="search" class="relative" @submit.prevent="submitForm">
      <label for="search-input" class="sr-only">Search people and posts</label>
      <Search class="pointer-events-none absolute left-5 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
      <input id="search-input" ref="input" type="search" v-model="query" autocomplete="off"
             class="field h-14 rounded-full pl-14 pr-28 text-base shadow-soft"
             placeholder="Search people or posts">
      <btn class="absolute right-2 top-1/2 -translate-y-1/2" type="submit" :loading="loading" :disabled="!query.trim()">
        Search
      </btn>
    </form>

    <div v-if="searched && !loading && hasResults" class="flex gap-1 rounded-full bg-muted p-1" role="group" aria-label="Filter results">
      <button v-for="tab in tabs" :key="tab.key" type="button" :aria-pressed="activeTab === tab.key"
              :class="['flex-1 rounded-full px-4 py-2 text-sm font-semibold transition-all',
                       activeTab === tab.key ? 'bg-card text-foreground shadow-soft' : 'text-muted-foreground hover:text-foreground']"
              @click="activeTab = tab.key">
        {{ tab.label }} <span class="ml-1 text-xs text-muted-foreground">{{ tab.count }}</span>
      </button>
    </div>

    <div v-if="loading" class="grid grid-cols-2 gap-3 sm:grid-cols-3" aria-hidden="true">
      <div v-for="n in 3" :key="n" class="surface flex flex-col items-center p-5">
        <div class="skeleton h-14 w-14 rounded-full" />
        <div class="skeleton mt-3 h-3.5 w-20" />
      </div>
    </div>

    <template v-else-if="searched && hasResults">
      <section v-if="activeTab === 'all' || activeTab === 'people'" v-show="users.length > 0" aria-label="People" class="space-y-3">
        <h2 v-if="activeTab === 'all'" class="eyebrow px-1">People</h2>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
          <PersonCard v-for="user in users" :key="user.id" :user="user" />
        </div>
      </section>
      <section v-if="activeTab === 'all' || activeTab === 'posts'" v-show="posts.length > 0" aria-label="Posts" class="space-y-4">
        <h2 v-if="activeTab === 'all'" class="eyebrow px-1 pt-2">Posts</h2>
        <FeedItem v-for="post in posts" :key="post.id" :post="post" @deletePost="deletePost" />
      </section>
    </template>

    <EmptyState v-else-if="searched && error" :icon="WifiOff" title="Search failed" description="Please try again in a moment." />

    <EmptyState v-else-if="searched" :icon="SearchX" :title="`No results for “${lastQuery}”`"
                description="Try a different name or keyword." />

    <EmptyState v-else :icon="Compass" title="Discover something new"
                description="Search for friends by name, or find posts by any word or #hashtag." />
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { Compass, Search, SearchX, WifiOff } from 'lucide-vue-next';
import FeedItem from '../components/FeedItem.vue';
import PersonCard from '@/components/PersonCard.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import btn from '../components/ui/Button.vue';
import { Post, User } from '@/interfaces';

type Tab = 'all' | 'people' | 'posts';

export default defineComponent({
  components: {
    FeedItem,
    PersonCard,
    PageLayout,
    PageHeader,
    EmptyState,
    Search,
    btn
  },
  setup() {
    return { Compass, SearchX, WifiOff };
  },
  data() {
    return {
      query: '',
      lastQuery: '',
      users: [] as User[],
      posts: [] as Post[],
      loading: false,
      searched: false,
      error: false,
      activeTab: 'all' as Tab
    };
  },
  computed: {
    hasResults(): boolean {
      return this.users.length > 0 || this.posts.length > 0;
    },
    tabs(): { key: Tab; label: string; count: number }[] {
      return [
        { key: 'all', label: 'All', count: this.users.length + this.posts.length },
        { key: 'people', label: 'People', count: this.users.length },
        { key: 'posts', label: 'Posts', count: this.posts.length },
      ];
    }
  },
  methods: {
    submitForm() {
      if (!this.query.trim()) {
        return;
      }
      this.loading = true;
      this.error = false;
      this.lastQuery = this.query.trim();
      axios.post('api/search/', {
        query: this.query
      }).then(response => {
        this.users = response.data.users;
        this.posts = response.data.posts;
        this.activeTab = 'all';
      }).catch(e => {
        this.error = true;
        this.users = [];
        this.posts = [];
        console.log('error', e);
      }).finally(() => {
        this.loading = false;
        this.searched = true;
      });
    },
    deletePost(postId: string) {
      this.posts = this.posts.filter(post => post.id != postId);
    }
  },
  mounted() {
    // avoid popping the on-screen keyboard on phones
    if (window.matchMedia('(min-width: 768px)').matches) {
      (this.$refs.input as HTMLInputElement).focus();
    }
  }
});
</script>
