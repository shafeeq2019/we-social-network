<template>
  <div class="group flex gap-3 animate-fade-up">
    <RouterLink :to="{ name: 'profile', params: { id: comment.created_by.id } }" class="shrink-0 rounded-full" tabindex="-1" aria-hidden="true">
      <Avatar :src="comment.created_by.avatar_link" :name="comment.created_by.name" size="sm" />
    </RouterLink>
    <div class="min-w-0 flex-1">
      <div class="inline-block max-w-full rounded-2xl rounded-tl-md bg-muted px-4 py-2.5">
        <RouterLink :to="{ name: 'profile', params: { id: comment.created_by.id } }"
                    class="text-sm font-semibold hover:underline underline-offset-2">
          {{ comment.created_by.name }}
        </RouterLink>
        <p class="whitespace-pre-line break-words text-[15px] leading-relaxed">{{ comment.comment }}</p>
      </div>
      <div class="mt-1 flex items-center gap-2 pl-3 text-xs text-muted-foreground">
        <time :datetime="comment.created_at">{{ formatAgo(comment.created_ago) }}</time>
      </div>
    </div>
    <DropdownMenu v-if="canDelete">
      <DropdownMenuTrigger class="icon-btn h-8 w-8 opacity-100 transition-opacity sm:opacity-0 sm:focus-visible:opacity-100 sm:group-hover:opacity-100 data-[state=open]:opacity-100"
                           aria-label="Comment options">
        <MoreHorizontal class="h-4 w-4" aria-hidden="true" />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" class="w-48 rounded-2xl p-1.5 shadow-lift">
        <DropdownMenuItem class="menu-item-danger cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="deleteComment">
          <Trash2 class="h-4 w-4" aria-hidden="true" /> Delete comment
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </div>
</template>

<script lang="ts">
import { Comment } from '../interfaces';
import {
  PropType,
  defineComponent,
} from 'vue';
import { MoreHorizontal, Trash2 } from 'lucide-vue-next';
import {
  useToastStore
} from '@/stores/toast';
import {
  useUserStore
} from '@/stores/user';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import Avatar from './ui/Avatar.vue';
import { formatAgo } from '@/lib/utils';

import axios from 'axios';
export default defineComponent({
  emits: ['deleteComment'],
  props: {
    comment: {
      type: Object as PropType<Comment>,
      required: true
    },
    postAuthorId: {
      type: String,
      required: false
    },
  },
  components: {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    Avatar,
    MoreHorizontal,
    Trash2,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
      formatAgo
    };
  },
  computed: {
    canDelete(): boolean {
      // The comment author and the post author can delete a comment
      const userId = this.userStore.user.id;
      return userId === this.comment.created_by.id || userId === this.postAuthorId;
    }
  },
  methods: {
    deleteComment() {
      axios.delete(`/api/post/${this.$route.params.id}/comment/${this.comment?.id}/`).then(
        () => {
          this.$emit('deleteComment', this.comment.id);
          this.toastStore.showToast(3000, 'Comment deleted', 'bg-emerald-500');
        }
      ).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'The comment could not be deleted.', 'bg-red-300');
      });
    },
  },
});
</script>
