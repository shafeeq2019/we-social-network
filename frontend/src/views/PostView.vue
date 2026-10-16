<template>
  <PageLayout>
    <div class="flex items-center gap-2 px-1">
      <button type="button" class="icon-btn -ml-2" aria-label="Go back" @click="$router.back()">
        <ArrowLeft class="h-5 w-5" aria-hidden="true" />
      </button>
      <h1 class="text-xl font-bold">Post</h1>
    </div>

    <PostSkeleton v-if="loading" />

    <EmptyState v-else-if="notFound" :icon="FileQuestion" title="This post isn't available"
                description="It may have been deleted, or it's only visible to its author.">
      <RouterLink :to="{ name: 'feed' }" class="text-sm font-semibold text-primary-soft-foreground hover:underline dark:text-primary">
        Back to your feed
      </RouterLink>
    </EmptyState>

    <template v-else-if="post.created_by">
      <FeedItem :post="post" />

      <section class="surface p-5" aria-labelledby="comments-title">
        <h2 id="comments-title" class="mb-4 flex items-center gap-2 text-base font-bold">
          Comments
          <span class="rounded-full bg-muted px-2 py-0.5 text-xs font-semibold text-muted-foreground">{{ post.comments.length }}</span>
        </h2>

        <form class="flex items-start gap-3" @submit.prevent="submitForm">
          <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" size="sm" />
          <div class="relative flex-1">
            <label for="comment-text" class="sr-only">Write a comment</label>
            <textarea id="comment-text" ref="commentInput" v-model="commentText" rows="1"
                      class="field min-h-[44px] resize-none rounded-3xl py-2.5 pr-14"
                      placeholder="Write a comment…" @input="autoGrow"
                      @keydown.enter.exact.prevent="submitForm"></textarea>
            <button type="submit" :disabled="!commentText.trim() || sending"
                    class="absolute bottom-1.5 right-1.5 flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground transition hover:brightness-110 disabled:opacity-40"
                    aria-label="Send comment">
              <Loader2 v-if="sending" class="h-4 w-4 animate-spin" aria-hidden="true" />
              <ArrowUp v-else class="h-4 w-4" :stroke-width="2.5" aria-hidden="true" />
            </button>
          </div>
        </form>

        <div v-if="post.comments.length > 0" class="mt-6 space-y-5">
          <CommentItem v-for="comment in post.comments" :key="comment.id" :comment="comment" @deleteComment="deleteComment" />
        </div>
        <p v-else class="mt-6 rounded-2xl bg-muted/60 px-4 py-6 text-center text-sm text-muted-foreground">
          No comments yet. Start the conversation.
        </p>
      </section>
    </template>
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { ArrowLeft, ArrowUp, FileQuestion, Loader2 } from 'lucide-vue-next';
import FeedItem from '../components/FeedItem.vue';
import CommentItem from '../components/CommentItem.vue';
import PostSkeleton from '@/components/PostSkeleton.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import Avatar from '@/components/ui/Avatar.vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { Comment, Post } from '../interfaces';

export default defineComponent({
  async beforeRouteUpdate() {
    // react to route changes...
    await this.getPost();
  },
  components: {
    FeedItem,
    CommentItem,
    PostSkeleton,
    PageLayout,
    EmptyState,
    Avatar,
    ArrowLeft,
    ArrowUp,
    Loader2,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return { userStore, toastStore, FileQuestion };
  },
  data() {
    return {
      post: {
        comments: [] as Comment[]
      } as Post & { comments: Comment[] },
      commentText: '',
      loading: true,
      sending: false,
      notFound: false
    };
  },
  methods: {
    async getPost() {
      await axios.get(`/api/post/${this.$route.params.id}/detail/`).then(response => {
        this.post = response.data.post;
        this.notFound = !this.post;
      }).catch(error => {
        this.notFound = true;
        console.log(error);
      }).finally(() => {
        this.loading = false;
      });
    },
    autoGrow() {
      const el = this.$refs.commentInput as HTMLTextAreaElement;
      el.style.height = 'auto';
      el.style.height = `${el.scrollHeight}px`;
    },
    async submitForm() {
      if (this.commentText.trim().length !== 0 && !this.sending) {
        this.sending = true;
        axios.post(`/api/post/${this.$route.params.id}/comment/`, {
          'comment': this.commentText
        }).then(async () => {
          this.commentText = '';
          (this.$refs.commentInput as HTMLTextAreaElement).style.height = '';
          await this.getPost();
        }).catch(error => {
          console.log(error);
          this.toastStore.showToast(4000, 'Your comment could not be posted.', 'bg-red-300');
        }).finally(() => {
          this.sending = false;
        });
      }
    },
    deleteComment(commentId: string) {
      this.post.comments = this.post.comments.filter(
        comment => comment.id != commentId
      );
      this.post.comments_count = Math.max(0, (this.post.comments_count ?? 1) - 1);
    }
  },
  created() {
    this.getPost();
  }
});
</script>
