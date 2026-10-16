<template>
  <!-- Compact horizontal strip for small screens -->
  <section v-if="variant === 'strip' && users.length > 0" aria-labelledby="pymk-strip-title" class="xl:hidden">
    <h2 id="pymk-strip-title" class="eyebrow mb-3 px-1">Suggested for you</h2>
    <ul class="no-scrollbar -mx-4 flex snap-x scroll-px-4 gap-3 overflow-x-auto px-4 pb-1 sm:-mx-6 sm:scroll-px-6 sm:px-6">
      <li v-for="user in users" :key="user.id" class="snap-start">
        <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
                    class="surface flex w-[132px] flex-col items-center px-3 py-4 text-center transition hover:-translate-y-0.5 hover:shadow-lift">
          <Avatar :src="user.avatar_link" :name="user.name" size="lg" />
          <span class="mt-3 line-clamp-1 w-full text-sm font-semibold">{{ user.name }}</span>
          <span class="text-xs text-muted-foreground">{{ user.friends_count }} friends</span>
        </RouterLink>
      </li>
    </ul>
  </section>

  <section v-else-if="variant === 'card' && (loading || users.length > 0)" class="surface p-5" aria-labelledby="pymk-title">
    <h2 id="pymk-title" class="mb-4 text-base font-bold">People you may know</h2>
    <ul v-if="loading" class="space-y-4" aria-hidden="true">
      <li v-for="n in 3" :key="n" class="flex items-center gap-3">
        <div class="skeleton h-11 w-11 rounded-full" />
        <div class="flex-1 space-y-2">
          <div class="skeleton h-3 w-28" />
          <div class="skeleton h-3 w-16" />
        </div>
      </li>
    </ul>
    <ul v-else class="-mx-2 space-y-1">
      <li v-for="user in users" :key="user.id">
        <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
                    class="group flex items-center gap-3 rounded-2xl p-2 transition-colors hover:bg-muted">
          <Avatar :src="user.avatar_link" :name="user.name" />
          <span class="min-w-0 flex-1">
            <span class="block truncate text-sm font-semibold">{{ user.name }}</span>
            <span class="block text-xs text-muted-foreground">{{ user.friends_count }} friends · {{ user.posts_count }} posts</span>
          </span>
          <span class="rounded-full bg-primary-soft px-3 py-1.5 text-xs font-semibold text-primary-soft-foreground transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
            View
          </span>
        </RouterLink>
      </li>
    </ul>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import axios from 'axios';
import { User } from '../interfaces';
import Avatar from '@/components/ui/Avatar.vue';

export default defineComponent({
  components: { Avatar },
  props: {
    variant: {
      type: String as PropType<'card' | 'strip'>,
      default: 'card'
    }
  },
  data() {
    return {
      users: [] as User[],
      loading: true
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
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
});
</script>
