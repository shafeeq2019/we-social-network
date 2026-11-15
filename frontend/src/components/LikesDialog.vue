<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogContent class="rounded-3xl sm:max-w-[400px]">
      <DialogHeader>
        <DialogTitle class="font-display text-xl font-bold">Liked by</DialogTitle>
        <DialogDescription class="sr-only">People who liked this post</DialogDescription>
      </DialogHeader>

      <div class="-mx-2 max-h-[60vh] overflow-y-auto px-2">
        <div v-if="loading && users.length === 0" class="flex justify-center py-8" role="status">
          <Loader2 class="h-5 w-5 animate-spin text-muted-foreground" aria-hidden="true" />
          <span class="sr-only">Loading likes</span>
        </div>

        <p v-else-if="error && users.length === 0" class="py-8 text-center text-sm text-muted-foreground">
          Couldn't load the likes.
          <button type="button" class="font-semibold text-foreground underline-offset-2 hover:underline" @click="load(1)">Try again</button>
        </p>

        <p v-else-if="users.length === 0" class="py-8 text-center text-sm text-muted-foreground">
          No likes yet.
        </p>

        <ul v-else class="space-y-0.5">
          <li v-for="user in users" :key="user.id">
            <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
                        class="flex items-center gap-3 rounded-2xl p-2 transition-colors hover:bg-muted"
                        @click="emit('update:open', false)">
              <Avatar :src="user.avatar_link" :name="user.name" size="sm" />
              <span class="min-w-0 flex-1 truncate font-semibold">
                {{ user.name }}
                <span v-if="user.id === userStore.user.id" class="font-normal text-muted-foreground">(you)</span>
              </span>
            </RouterLink>
          </li>
        </ul>

        <div v-if="hasNext && users.length > 0" class="flex justify-center pt-3">
          <btn variant="ghost" size="sm" :loading="loading" @click="load(page + 1)">Show more</btn>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';
import { Loader2 } from 'lucide-vue-next';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import Avatar from '@/components/ui/Avatar.vue';
import btn from '@/components/ui/Button.vue';
import { useUserStore } from '@/stores/user';
import type { User } from '@/interfaces';

const props = defineProps<{ postId: string; open: boolean }>();
const emit = defineEmits<{ 'update:open': [value: boolean] }>();

const userStore = useUserStore();
const users = ref<User[]>([]);
const page = ref(1);
const hasNext = ref(false);
const loading = ref(false);
const error = ref(false);

async function load(nextPage: number) {
  loading.value = true;
  error.value = false;
  try {
    const response = await axios.get(`/api/post/${props.postId}/likes/?page=${nextPage}`);
    users.value = nextPage === 1 ? response.data.results : [...users.value, ...response.data.results];
    page.value = nextPage;
    hasNext.value = !!response.data.next;
  } catch (e) {
    console.log(e);
    error.value = true;
  } finally {
    loading.value = false;
  }
}

// Reload on every open, so likes made in the meantime show up
watch(() => props.open, (isOpen) => {
  if (isOpen) {
    users.value = [];
    load(1);
  }
});
</script>
