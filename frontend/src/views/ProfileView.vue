<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- User on the left -->
        <div class="main-left col-span-4 md:col-span-1 order-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="flex items-center justify-center ">
                    <img :src="user.avatar_link"
                        class="mb-6 w-[220px] max-h-60 md:max-h-36 lg:max-h-60 rounded-full object-cover object-center" />
                </div>

                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <router-link :to="{name:'friends', params:{id: user.id}}" class="text-xs text-gray-500">
                        {{user.friends_count}} friends</router-link>
                    <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
                </div>
                <div class="mt-6 space-y-2">
                    <router-link v-if="user.id == userStore.user.id" :to="{name:'editprofile'}"
                        class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full">
                        Edit profile
                    </router-link>

                    <DropdownMenu v-if="user.id != userStore.user.id && isFriends">
                        <DropdownMenuTrigger
                            class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full flex justify-center items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                            </svg>
                            <p>Friends</p>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <!-- <DropdownMenuSeparator /> -->
                            <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center p-1"
                                @click="deleteFriendshipRequest">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M22 10.5h-6m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM4 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 10.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                                </svg>

                                <p>Remove friendship with {{user.name}}</p>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu
                        v-if="user.id != userStore.user.id && friendship_request.status === 'sent' && friendship_request.created_by.id == userStore.user.id">
                        <DropdownMenuTrigger
                            class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full flex justify-center items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                            </svg>
                            <p>Friendship request sent</p>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <!-- <DropdownMenuSeparator /> -->
                            <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center p-1"
                                @click="handleFriendshipRequest('canceled')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M22 10.5h-6m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM4 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 10.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                                </svg>

                                <p>Cancel friend request</p>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu
                        v-if="user.id != userStore.user.id && friendship_request.status === 'sent' && friendship_request.created_by.id == user.id">
                        <DropdownMenuTrigger
                            class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full flex justify-center items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                            </svg>
                            <p>{{user.name}} want to be your friend</p>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center p-1"
                                @click="handleFriendshipRequest('accepted')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                                </svg>

                                <p>Accept friend request</p>
                            </DropdownMenuItem>
                            <!-- <DropdownMenuSeparator /> -->
                            <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center p-1"
                                @click="handleFriendshipRequest('rejected')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                </svg>
                                <p>Reject friend request</p>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <button v-if="user.id != userStore.user.id && !isFriends && friendship_request.status != 'sent'"
                        class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full flex justify-center items-center space-x-2"
                        @click="sendFriendshipRequest()">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
                        </svg>
                        <p>Send friendship request </p>
                    </button>

                    <button v-if="user.id != userStore.user.id"
                        class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full flex justify-center items-center space-x-2"
                        @click="sendDirectMessage">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                        </svg>
                        <p>Send direct message</p>
                    </button>
                </div>
            </div>
        </div>
        <!-- New post & feeds on the middle -->
        <div class="main-center space-y-4 col-span-4 md:col-span-2 order-3 md:order-2">
            <FeedForm :user="user" v-if="userStore.user.id == user.id" :posts="posts" />
            <div  v-if="posts.length > 0" class="space-y-4">
                <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost"/>
            </div>

            <div v-else-if="!loading" class="bg-white shadow-md sm:rounded-lg p-6">
                <div class="text-center">

                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="h-36 w-40 text-purple-600 mx-auto ">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
                    </svg>

                    <p class="mt-2 text-xl font-semibold text-gray-700">{{user.name}} has not published any posts yet
                    </p>
                </div>
            </div>
        </div>

        <!-- People you may know -->
        <div class="main-right space-y-4 col-span-4 md:col-span-1 order-2 md:order-3">
            <PeopleYouMayKnow />
            <Trends />
        </div>

    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trends from '../components/Trends.vue';
import { useUserStore } from '@/stores/user';
import FeedItem from '../components/FeedItem.vue';
import { useToastStore } from "@/stores/toast";
import { User, Post, FriendshipRequest } from '../interfaces';
import FeedForm from '@/components/FeedForm.vue';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export default defineComponent({
  async beforeRouteUpdate(to) {
    this.posts = [];
    // react to route changes...
    await this.getFeeds(to.params.id);
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore
    };
  },
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    FeedForm,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  },
  data() {
    return {
      posts: [] as Post[],
      user: {} as User,
      friendship_request: {} as FriendshipRequest,
      isFriends: false,
      currentPage: 1,
      hasNext: true,
      loading: true

    };
  },
  computed: {

  },
  methods: {
    async sendDirectMessage() {
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
      });
    },
    async getFeeds(userId: string | string[]) {
      await axios.get(`/api/post/profile/${userId}/?page=${this.currentPage}`).then(response => {
        if (response.data.next) {
          this.hasNext = true;
        }
        this.loading = false;
        this.posts = [...this.posts, ...response.data.results.posts];
        this.user = response.data.results.user;
        this.friendship_request = response.data.results.friendship_request;
        this.isFriends = response.data.results.friends;
      }).catch(error => {
        this.loading = false;
        console.log(error);
      });
    },
    async sendFriendshipRequest() {
      axios.post(`/api/friends/${this.$route.params.id}/request/`, {
      }).then(response => {
        if (response.data.id) {
          this.friendship_request = response.data;
          this.toastStore.showToast(5000, "The request was sent!", "bg-emerald-300");
        }
      }).catch(error => {
        console.log(error);
      });
    },
    async deleteFriendshipRequest() {
      axios.delete(`/api/friends/${this.$route.params.id}/request/`, {
      }).then(response => {
        if (response.data.message == "friendship removed") {
          this.isFriends = false;
          this.friendship_request = {} as FriendshipRequest;
          this.user.friends_count -= 1;
          this.toastStore.showToast(5000, "Friendship removed!", "bg-emerald-300");
        }
      }).catch(error => {
        console.log(error);
      });
    },
    async handleFriendshipRequest(status: string) {
      axios.post(`/api/friends/${this.$route.params.id}/request/${this.friendship_request.id}/`, {
        status
      }).then(response => {
        this.friendship_request = response.data;
        if (status === 'accepted') {
          this.isFriends = true;
          this.user.friends_count += 1;
          this.toastStore.showToast(5000, `You are now friends with ${this.user.name}!`, "bg-emerald-300");
        }
      }).catch(error => {
        console.log(error);
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
    const onScroll = () => {
      const bottomOfWindow = parseInt(`${document.documentElement.scrollTop + window.innerHeight}`) === document.documentElement.offsetHeight;
      if (bottomOfWindow && this.hasNext) {
        this.currentPage += 1;
        this.hasNext = false;
        this.getFeeds(this.$route.params.id);
      }
    };
    this.getFeeds(this.$route.params.id);
    window.onscroll = onScroll;
    window.ontouchmove = onScroll;
  }
});
</script>