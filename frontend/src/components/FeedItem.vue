<template>
  <article class="surface animate-fade-up overflow-hidden" :aria-labelledby="`post-${post.id}-author`">
    <header class="flex items-start gap-3 px-5 pt-5">
      <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }" class="shrink-0 rounded-full" tabindex="-1" aria-hidden="true">
        <Avatar :src="post.created_by.avatar_link" :name="post.created_by.name" />
      </RouterLink>
      <div class="min-w-0 flex-1 pt-0.5">
        <RouterLink :id="`post-${post.id}-author`" :to="{ name: 'profile', params: { id: post.created_by.id } }"
                    class="block truncate font-semibold leading-tight hover:underline underline-offset-2">
          {{ post.created_by.name }}
        </RouterLink>
        <p class="mt-0.5 flex items-center gap-1.5 text-[13px] text-muted-foreground">
          <RouterLink :to="{ name: 'postview', params: { id: post.id } }" class="hover:underline underline-offset-2">
            <time :datetime="post.created_at">{{ formatAgo(post.created_ago) }}</time>
          </RouterLink>
          <span v-if="post.is_private !== undefined" aria-hidden="true">·</span>
          <span v-if="post.is_private !== undefined" class="inline-flex items-center gap-1">
            <Lock v-if="post.is_private" class="h-3.5 w-3.5" aria-hidden="true" />
            <Globe2 v-else class="h-3.5 w-3.5" aria-hidden="true" />
            {{ post.is_private ? 'Only you' : 'Public' }}
          </span>
        </p>
      </div>

      <DropdownMenu>
        <DropdownMenuTrigger class="icon-btn -mr-2 -mt-1" aria-label="Post options">
          <MoreHorizontal class="h-5 w-5" aria-hidden="true" />
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="w-48 rounded-2xl p-1.5 shadow-lift">
          <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="copyLink">
            <Link2 class="h-4 w-4 text-muted-foreground" aria-hidden="true" /> Copy link
          </DropdownMenuItem>
          <DropdownMenuItem v-if="isOwner" class="menu-item-danger cursor-pointer gap-3 rounded-xl px-2.5 py-2"
                            @select="openDeleteModal = true">
            <Trash2 class="h-4 w-4" aria-hidden="true" /> Delete post
          </DropdownMenuItem>
          <DropdownMenuItem v-else class="cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="openReportModal = true">
            <Flag class="h-4 w-4 text-muted-foreground" aria-hidden="true" /> Report
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </header>

    <div v-if="post.body" class="post-text whitespace-pre-line break-words px-5 pt-3 text-[15.5px] leading-relaxed"
         v-html="renderRichText(post.body)" @click="onBodyClick" />

    <RouterLink v-if="post.post_attachments && post.post_attachments.length > 0"
                :to="{ name: 'postview', params: { id: post.id } }"
                class="mx-5 mt-4 block overflow-hidden rounded-2xl border border-border/60 bg-muted">
      <img :src="post.post_attachments[0].image_link" :key="post.post_attachments[0].id"
           :alt="`Image shared by ${post.created_by.name}`" loading="lazy"
           class="max-h-[560px] w-full object-cover transition-transform duration-500 hover:scale-[1.015]">
    </RouterLink>

    <footer class="flex items-center gap-1 px-3 pb-3 pt-3">
      <button type="button" @click="likePost" :aria-pressed="post.post_liked"
              :aria-label="post.post_liked ? 'Unlike post' : 'Like post'"
              :class="['group inline-flex h-10 items-center gap-2 rounded-full px-3 text-sm font-semibold transition-colors',
                       post.post_liked ? 'text-like hover:bg-like/10' : 'text-muted-foreground hover:bg-like/10 hover:text-like']">
        <Heart :key="likeAnimKey" :class="['h-5 w-5', likeAnimKey > 0 && post.post_liked ? 'animate-pop' : '']"
               :fill="post.post_liked ? 'currentColor' : 'none'" aria-hidden="true" />
        <span class="tabular-nums">{{ post.likes_count }}</span>
      </button>

      <RouterLink :to="{ name: 'postview', params: { id: post.id } }"
                  class="inline-flex h-10 items-center gap-2 rounded-full px-3 text-sm font-semibold text-muted-foreground transition-colors hover:bg-primary/10 hover:text-primary-soft-foreground dark:hover:text-primary"
                  :aria-label="`${post.comments_count ?? 0} comments, open post`">
        <MessageCircle class="h-5 w-5" aria-hidden="true" />
        <span class="tabular-nums">{{ post.comments_count ?? 0 }}</span>
      </RouterLink>

      <button type="button" @click="share"
              class="ml-auto inline-flex h-10 items-center gap-2 rounded-full px-3 text-sm font-semibold text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
        <Share2 class="h-[18px] w-[18px]" aria-hidden="true" />
        <span class="hidden sm:inline">Share</span>
        <span class="sr-only sm:hidden">Share post</span>
      </button>
    </footer>

    <Dialog v-model:open="openReportModal" @update:open="reportText = ''">
      <DialogContent class="rounded-3xl sm:max-w-[440px]">
        <DialogHeader>
          <DialogTitle class="font-display text-xl font-bold">Report this post</DialogTitle>
          <DialogDescription class="text-muted-foreground">
            Tell us what's wrong. Reports are anonymous and reviewed by our team.
          </DialogDescription>
        </DialogHeader>
        <label for="report-text" class="sr-only">Reason</label>
        <textarea id="report-text" class="field min-h-[120px] resize-none" placeholder="Why should this post be removed?"
                  v-model="reportText"></textarea>
        <DialogFooter class="gap-2">
          <btn variant="ghost" type="button" @click="openReportModal = false">Cancel</btn>
          <btn type="button" :loading="reporting" :disabled="!reportText.trim()" @click="reportPost">Send report</btn>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="openDeleteModal">
      <DialogContent class="rounded-3xl sm:max-w-[400px]">
        <DialogHeader>
          <DialogTitle class="font-display text-xl font-bold">Delete post?</DialogTitle>
          <DialogDescription class="text-muted-foreground">
            This can't be undone. The post, its likes and comments will be removed.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter class="gap-2">
          <btn variant="ghost" type="button" @click="openDeleteModal = false">Cancel</btn>
          <btn variant="destructive" type="button" :loading="deleting" @click="deletePost">Delete</btn>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </article>
</template>

<script lang="ts">
import {
  defineComponent
} from 'vue';
import axios from 'axios';
import {
  Post
} from '../interfaces.ts';
import type {
  PropType
} from 'vue';
import {
  Flag, Globe2, Heart, Link2, Lock, MessageCircle, MoreHorizontal, Share2, Trash2
} from 'lucide-vue-next';
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import btn from './ui/Button.vue';
import Avatar from './ui/Avatar.vue';
import { formatAgo, renderRichText } from '@/lib/utils';

export default defineComponent({
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    btn,
    Avatar,
    Flag,
    Globe2,
    Heart,
    Link2,
    Lock,
    MessageCircle,
    MoreHorizontal,
    Share2,
    Trash2,
  },
  emits: ['deletePost'],
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
      formatAgo,
      renderRichText
    };
  },
  props: {
    post: {
      type: Object as PropType<Post>,
      required: true
    }
  },
  data() {
    return {
      openReportModal: false,
      openDeleteModal: false,
      reportText: '',
      reporting: false,
      deleting: false,
      liking: false,
      likeAnimKey: 0
    };
  },
  computed: {
    isOwner(): boolean {
      return this.userStore.user.id === this.post.created_by.id;
    },
    absoluteURL(): string {
      const route = this.$router.resolve({ name: 'postview', params: { id: this.post.id } });
      return new URL(route.href, window.location.origin).href;
    }
  },
  methods: {
    likePost() {
      if (this.liking) {
        return;
      }
      this.liking = true;
      this.likeAnimKey += 1;
      axios.post(`/api/post/${this.post.id}/like/`).then(response => {
        /* eslint-disable */
        if (response.data.message == 'post liked successfully') {
          this.post.likes_count += 1;
          this.post.post_liked = true;
        } else {
          this.post.likes_count -= 1;
          this.post.post_liked = false;
        }
        /* eslint-enable */
      }).catch(e => {
        console.log(e);
        this.toastStore.showToast(4000, 'Could not update your like. Please try again.', 'bg-red-300');
      }).finally(() => {
        this.liking = false;
      });
    },
    onBodyClick(event: MouseEvent) {
      const target = (event.target as HTMLElement).closest('a[data-hashtag]') as HTMLAnchorElement | null;
      if (target) {
        event.preventDefault();
        this.$router.push({ name: 'trendsview', params: { hashtag: target.dataset.hashtag } });
      }
    },
    async deletePost() {
      this.deleting = true;
      axios.delete(`/api/post/${this.post.id}`).then(
        () => {
          this.openDeleteModal = false;
          this.$emit('deletePost', this.post.id);
          this.toastStore.showToast(5000, 'The post was deleted', 'bg-emerald-500');
          if (this.$route.name == 'postview') {
            this.$router.go(-1);
          }
        }
      ).catch(e => {
        console.log(e);
        this.toastStore.showToast(5000, 'The post could not be deleted.', 'bg-red-300');
      }).finally(() => {
        this.deleting = false;
      });
    },
    async reportPost() {
      this.reporting = true;
      axios.post(`/api/post/${this.post.id}/report/`, {
        reportText: this.reportText
      }).then(() => {
        this.openReportModal = false;
        this.toastStore.showToast(5000, 'Thanks — the post was reported', 'bg-emerald-500');
      }).catch(e => {
        console.log(e);
        this.toastStore.showToast(5000, 'The report could not be sent.', 'bg-red-300');
      }).finally(() => {
        this.reporting = false;
      });
    },
    async copyLink() {
      try {
        await navigator.clipboard.writeText(this.absoluteURL);
        this.toastStore.showToast(3000, 'Link copied to clipboard', 'bg-emerald-500');
      } catch (e) {
        console.log(e);
        this.toastStore.showToast(4000, 'Could not copy the link', 'bg-red-300');
      }
    },
    async share() {
      if (navigator.share) {
        try {
          await navigator.share({
            title: 'Post from We',
            text: this.post.body,
            url: this.absoluteURL,
          });
        } catch {
          // the user dismissed the share sheet
        }
      } else {
        this.copyLink();
      }
    }
  }
});
</script>
