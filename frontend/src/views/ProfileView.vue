<template>
  <PageLayout>
    <!-- Profile header -->
    <section v-if="loading && !user.id" class="surface overflow-hidden" aria-hidden="true">
      <div class="skeleton h-36 rounded-none sm:h-48" />
      <div class="px-5 pb-6 sm:px-7">
        <div class="skeleton -mt-12 h-28 w-28 rounded-full ring-4 ring-card" />
        <div class="skeleton mt-4 h-6 w-48" />
        <div class="skeleton mt-3 h-4 w-32" />
      </div>
    </section>

    <section v-else-if="user.id" class="surface overflow-hidden" aria-labelledby="profile-name">
      <div class="relative h-36 overflow-hidden bg-primary-soft sm:h-48">
        <img v-if="user.avatar_link" :src="user.avatar_link" alt=""
             class="absolute inset-0 h-full w-full scale-125 object-cover opacity-80 blur-3xl saturate-150" aria-hidden="true">
        <div class="absolute inset-0 bg-gradient-to-t from-card/70 via-transparent to-transparent" aria-hidden="true" />
        <div class="absolute inset-0 opacity-[0.35] [background-image:radial-gradient(hsl(var(--card))_1px,transparent_1px)] [background-size:14px_14px]" aria-hidden="true" />
      </div>

      <div class="px-5 pb-6 sm:px-7">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <Avatar :src="user.avatar_link" :name="user.name" :alt="`${user.name}'s profile picture`" size="2xl" ring
                  class="-mt-14 shadow-lift sm:-mt-16" />

          <div class="flex flex-wrap gap-2 sm:pb-1">
            <template v-if="isOwnProfile">
              <RouterLink :to="{ name: 'editprofile' }"
                          class="inline-flex h-10 items-center gap-2 rounded-full border border-border bg-card px-4 text-sm font-semibold transition hover:bg-muted">
                <PenLine class="h-4 w-4" aria-hidden="true" /> Edit profile
              </RouterLink>
            </template>

            <template v-else>
              <!-- Friends -->
              <DropdownMenu v-if="isFriends">
                <DropdownMenuTrigger as-child>
                  <btn variant="soft">
                    <UserCheck class="h-4 w-4" aria-hidden="true" /> Friends
                    <ChevronDown class="h-3.5 w-3.5" aria-hidden="true" />
                  </btn>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" class="w-60 rounded-2xl p-1.5 shadow-lift">
                  <DropdownMenuItem class="menu-item-danger cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="deleteFriendshipRequest">
                    <UserMinus class="h-4 w-4" aria-hidden="true" /> Remove {{ firstName }} as friend
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <!-- Request sent by me -->
              <DropdownMenu v-else-if="requestSentByMe">
                <DropdownMenuTrigger as-child>
                  <btn variant="secondary">
                    <Clock class="h-4 w-4" aria-hidden="true" /> Request sent
                    <ChevronDown class="h-3.5 w-3.5" aria-hidden="true" />
                  </btn>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" class="w-56 rounded-2xl p-1.5 shadow-lift">
                  <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="handleFriendshipRequest('canceled')">
                    <X class="h-4 w-4 text-muted-foreground" aria-hidden="true" /> Cancel request
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <!-- Request received -->
              <template v-else-if="requestSentToMe">
                <btn :loading="pending === 'accepted'" @click="handleFriendshipRequest('accepted')">
                  <Check v-if="pending !== 'accepted'" class="h-4 w-4" aria-hidden="true" /> Accept
                </btn>
                <btn variant="outline" :loading="pending === 'rejected'" @click="handleFriendshipRequest('rejected')">Decline</btn>
              </template>

              <btn v-else :loading="pending === 'send'" @click="sendFriendshipRequest()">
                <UserPlus v-if="pending !== 'send'" class="h-4 w-4" aria-hidden="true" /> Add friend
              </btn>

              <btn variant="outline" :loading="pending === 'message'" @click="sendDirectMessage">
                <MessageCircle v-if="pending !== 'message'" class="h-4 w-4" aria-hidden="true" /> Message
              </btn>
            </template>
          </div>
        </div>

        <h1 id="profile-name" class="mt-4 break-words text-[26px] font-extrabold leading-tight sm:text-3xl">{{ user.name }}</h1>
        <p v-if="requestSentToMe" class="mt-1 text-sm font-medium text-primary-soft-foreground dark:text-primary">
          {{ firstName }} wants to be your friend
        </p>

        <dl class="mt-4 flex gap-6 text-sm">
          <div>
            <dt class="sr-only">Posts</dt>
            <dd><span class="font-display text-lg font-bold">{{ user.posts_count }}</span> <span class="text-muted-foreground">posts</span></dd>
          </div>
          <div>
            <dt class="sr-only">Friends</dt>
            <dd>
              <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="group hover:underline underline-offset-2">
                <span class="font-display text-lg font-bold">{{ user.friends_count }}</span> <span class="text-muted-foreground group-hover:text-foreground">friends</span>
              </RouterLink>
            </dd>
          </div>
        </dl>
      </div>
    </section>

    <EmptyState v-else :icon="UserX" title="Profile not found" description="This account may have been removed." />

    <template v-if="user.id">
      <FeedForm :user="user" v-if="isOwnProfile" :posts="posts" />

      <h2 class="eyebrow px-1 pt-2">Posts</h2>

      <div v-if="loading && posts.length === 0" class="space-y-4">
        <PostSkeleton v-for="n in 2" :key="n" />
      </div>
      <div v-else-if="posts.length > 0" class="space-y-4">
        <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost" />
      </div>
      <EmptyState v-else :icon="NotebookPen"
                  :title="isOwnProfile ? 'Share your first post' : 'No posts yet'"
                  :description="isOwnProfile ? 'Your posts will appear here for friends to see.' : `${firstName} hasn't shared anything yet.`" />

      <div v-if="loadingMore" class="flex justify-center py-6" role="status">
        <Loader2 class="h-5 w-5 animate-spin text-muted-foreground" aria-hidden="true" />
        <span class="sr-only">Loading more posts</span>
      </div>
    </template>
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import {
  Check, ChevronDown, Clock, Loader2, MessageCircle, NotebookPen, PenLine, UserCheck, UserMinus, UserPlus, UserX, X
} from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import FeedItem from '../components/FeedItem.vue';
import { useToastStore } from '@/stores/toast';
import { User, Post, FriendshipRequest } from '../interfaces';
import FeedForm from '@/components/FeedForm.vue';
import PostSkeleton from '@/components/PostSkeleton.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import Avatar from '@/components/ui/Avatar.vue';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import btn from '@/components/ui/Button.vue';
import { useInfiniteScroll } from '@/lib/infiniteScroll';

export default defineComponent({
  async beforeRouteUpdate(to) {
    this.posts = [];
    this.currentPage = 1;
    this.loading = true;
    // react to route changes...
    await this.getFeeds(to.params.id);
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
      NotebookPen,
      UserX
    };
  },
  components: {
    FeedItem,
    FeedForm,
    PostSkeleton,
    PageLayout,
    EmptyState,
    Avatar,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    btn,
    Check,
    ChevronDown,
    Clock,
    Loader2,
    MessageCircle,
    PenLine,
    UserCheck,
    UserMinus,
    UserPlus,
    X,
  },
  data() {
    return {
      posts: [] as Post[],
      user: {} as User,
      friendship_request: {} as FriendshipRequest,
      isFriends: false,
      currentPage: 1,
      hasNext: true,
      loading: true,
      loadingMore: false,
      pending: '' as string
    };
  },
  computed: {
    isOwnProfile(): boolean {
      return this.user.id == this.userStore.user.id;
    },
    firstName(): string {
      return (this.user.name || '').split(' ')[0];
    },
    requestSentByMe(): boolean {
      return this.friendship_request?.status === 'sent' && this.friendship_request.created_by?.id == this.userStore.user.id;
    },
    requestSentToMe(): boolean {
      return this.friendship_request?.status === 'sent' && this.friendship_request.created_by?.id == this.user.id;
    }
  },
  methods: {
    async sendDirectMessage() {
      this.pending = 'message';
      axios.post(`/api/chat/${this.$route.params.id}/`).then(
        () => {
          this.$router.push({
            name: 'messages',
            params: {
              user_id: this.$route.params.id
            }
          });
        }
      ).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'Could not open the conversation.', 'bg-red-300');
      }).finally(() => {
        this.pending = '';
      });
    },
    async getFeeds(userId: string | string[]) {
      await axios.get(`/api/post/profile/${userId}/?page=${this.currentPage}`).then(response => {
        this.hasNext = !!response.data.next;
        this.posts = [...this.posts, ...response.data.results.posts];
        this.user = response.data.results.user;
        this.friendship_request = response.data.results.friendship_request;
        this.isFriends = response.data.results.friends;
      }).catch(error => {
        console.log(error);
      }).finally(() => {
        this.loading = false;
        this.loadingMore = false;
      });
    },
    async sendFriendshipRequest() {
      this.pending = 'send';
      axios.post(`/api/friends/${this.$route.params.id}/request/`, {
      }).then(response => {
        if (response.data.id) {
          this.friendship_request = response.data;
          this.toastStore.showToast(5000, 'Friend request sent', 'bg-emerald-300');
        }
      }).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'The request could not be sent.', 'bg-red-300');
      }).finally(() => {
        this.pending = '';
      });
    },
    async deleteFriendshipRequest() {
      axios.delete(`/api/friends/${this.$route.params.id}/request/`, {
      }).then(response => {
        if (response.data.message == 'friendship removed') {
          this.isFriends = false;
          this.friendship_request = {} as FriendshipRequest;
          this.user.friends_count -= 1;
          this.toastStore.showToast(5000, 'Friendship removed', 'bg-emerald-300');
        }
      }).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'Something went wrong. Please try again.', 'bg-red-300');
      });
    },
    async handleFriendshipRequest(status: string) {
      this.pending = status;
      axios.post(`/api/friends/${this.$route.params.id}/request/${this.friendship_request.id}/`, {
        status
      }).then(response => {
        this.friendship_request = response.data;
        if (status === 'accepted') {
          this.isFriends = true;
          this.user.friends_count += 1;
          this.toastStore.showToast(5000, `You are now friends with ${this.user.name}!`, 'bg-emerald-300');
        }
      }).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'Something went wrong. Please try again.', 'bg-red-300');
      }).finally(() => {
        this.pending = '';
      });
    },
    deletePost(postId: string) {
      this.posts = this.posts.filter(
        post => post.id != postId
      );
      this.user.posts_count -= 1;
    }
  },
  mounted() {
    this.getFeeds(this.$route.params.id);
    useInfiniteScroll(() => {
      if (this.hasNext && !this.loading && !this.loadingMore) {
        this.currentPage += 1;
        this.loadingMore = true;
        this.getFeeds(this.$route.params.id);
      }
    });
  }
});
</script>
