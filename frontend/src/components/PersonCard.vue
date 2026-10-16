<template>
  <div class="surface group relative flex flex-col items-center p-5 text-center transition duration-200 hover:-translate-y-0.5 hover:shadow-lift">
    <Avatar :src="user.avatar_link" :name="user.name" size="lg" />
    <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
                class="mt-3 line-clamp-1 w-full break-all font-semibold after:absolute after:inset-0 after:rounded-3xl hover:underline underline-offset-2">
      {{ user.name }}
    </RouterLink>
    <p class="mt-0.5 text-xs text-muted-foreground">
      {{ user.friends_count }} {{ user.friends_count === 1 ? 'friend' : 'friends' }} · {{ user.posts_count }} {{ user.posts_count === 1 ? 'post' : 'posts' }}
    </p>
    <div v-if="$slots.actions" class="relative z-10 mt-4 flex w-full gap-2">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Avatar from '@/components/ui/Avatar.vue';
import type { User } from '@/interfaces';

defineProps<{ user: User }>();
</script>
