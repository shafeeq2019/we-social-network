<template>
  <PageLayout>
    <header class="flex items-center gap-3 px-1">
      <RouterLink v-if="user.id" :to="{ name: 'profile', params: { id: user.id } }" class="rounded-full" :aria-label="`Back to ${user.name}'s profile`">
        <Avatar :src="user.avatar_link" :name="user.name" size="lg" />
      </RouterLink>
      <div v-else class="skeleton h-14 w-14 rounded-full" aria-hidden="true" />
      <div class="min-w-0">
        <p class="eyebrow">{{ isOwn ? 'Your circle' : user.name }}</p>
        <h1 class="text-[28px] font-extrabold leading-tight sm:text-[32px]">Friends</h1>
        <p v-if="user.id" class="text-sm text-muted-foreground">{{ user.friends_count }} friends · {{ user.posts_count }} posts</p>
      </div>
    </header>

    <div v-if="loading" class="grid grid-cols-2 gap-3 sm:grid-cols-3" aria-hidden="true">
      <div v-for="n in 6" :key="n" class="surface flex flex-col items-center p-5">
        <div class="skeleton h-14 w-14 rounded-full" />
        <div class="skeleton mt-3 h-3.5 w-20" />
        <div class="skeleton mt-2 h-3 w-24" />
      </div>
    </div>

    <template v-else>
      <section v-if="friendship_requests.length > 0" aria-labelledby="requests-title" class="space-y-3">
        <h2 id="requests-title" class="flex items-center gap-2 px-1 text-base font-bold">
          Friend requests
          <span class="rounded-full bg-like px-2 py-0.5 text-xs font-bold text-white">{{ friendship_requests.length }}</span>
        </h2>
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <TransitionGroup enter-from-class="opacity-0 scale-95" leave-to-class="opacity-0 scale-95"
                           enter-active-class="transition duration-200" leave-active-class="transition duration-200">
            <PersonCard v-for="friendshipRequest in friendship_requests" :key="friendshipRequest.id" :user="friendshipRequest.created_by">
              <template #actions>
                <btn size="sm" class="flex-1" :loading="pendingId === friendshipRequest.id + 'accepted'"
                     @click="handleRequest('accepted', friendshipRequest)">
                  Accept
                </btn>
                <btn size="sm" variant="outline" class="flex-1" :loading="pendingId === friendshipRequest.id + 'rejected'"
                     @click="handleRequest('rejected', friendshipRequest)">
                  Decline
                </btn>
              </template>
            </PersonCard>
          </TransitionGroup>
        </div>
      </section>

      <section aria-labelledby="friends-title" class="space-y-3">
        <h2 v-if="friendship_requests.length > 0 || friends.length > 0" id="friends-title" class="px-1 text-base font-bold">
          All friends
        </h2>
        <div v-if="friends.length > 0" class="grid grid-cols-2 gap-3 sm:grid-cols-3">
          <PersonCard v-for="friend in friends" :key="friend.id" :user="friend" />
        </div>
        <EmptyState v-else :icon="Users" :title="isOwn ? 'No friends yet' : 'No friends to show'"
                    :description="isOwn ? 'Find people you know and send them a friend request.' : `${user.name} hasn't added any friends yet.`">
          <RouterLink v-if="isOwn" :to="{ name: 'search' }"
                      class="inline-flex h-10 items-center gap-2 rounded-full bg-foreground px-5 text-sm font-semibold text-background transition hover:bg-foreground/85">
            <Search class="h-4 w-4" aria-hidden="true" /> Find people
          </RouterLink>
        </EmptyState>
      </section>
    </template>
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { Search, Users } from 'lucide-vue-next';
import PersonCard from '@/components/PersonCard.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import Avatar from '@/components/ui/Avatar.vue';
import {
  useUserStore
} from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { FriendshipRequest, User } from '@/interfaces';
import btn from '@/components/ui/Button.vue';
export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
      Users
    };
  },
  components: {
    PersonCard,
    PageLayout,
    EmptyState,
    Avatar,
    Search,
    btn
  },
  data() {
    return {
      user: {} as User,
      friendship_requests: [] as FriendshipRequest[],
      friends: [] as User[],
      loading: true,
      pendingId: ''
    };
  },
  computed: {
    isOwn(): boolean {
      return this.$route.params.id === this.userStore.user.id;
    }
  },
  methods: {
    async getFriends() {
      await axios.get(`/api/friends/${this.$route.params.id}/`).then(response => {
        this.friendship_requests = response.data.requests;
        this.friends = response.data.friends;
        this.user = response.data.user;
      }).catch(error => {
        console.log(error);
      }).finally(() => {
        this.loading = false;
      });
    },
    async handleRequest(status: string, friendship_request: FriendshipRequest) {
      this.pendingId = friendship_request.id + status;
      axios.post(`/api/friends/${friendship_request.created_by.id}/request/${friendship_request.id}/`, {
        status
      }).then(async () => {
        await this.getFriends();
        if (status === 'accepted') {
          this.toastStore.showToast(4000, `You are now friends with ${friendship_request.created_by.name}`, 'bg-emerald-500');
        }
      }).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'Something went wrong. Please try again.', 'bg-red-300');
      }).finally(() => {
        this.pendingId = '';
      });
    },

  },
  created() {
    this.getFriends();
  }
});
</script>
