<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-4 xl:grid-cols-4 gap-4">
        <!-- User on the left -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-foreground text-primary border border-border text-center rounded-lg">
                <div class="flex items-center justify-center">
                    <img :src="user.avatar_link"
                        class="mb-6 w-[220px] max-h-60 md:max-h-36 lg:max-h-60 rounded-full object-cover object-center" />
                </div>

                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-secondary">{{user.friends_count}} friends</p>
                    <p class="text-xs text-secondary">{{user.posts_count}} posts</p>
                </div>
            </div>
        </div>

        <div class="main-center lg:col-span-2 space-y-4 text-primary">
            <div class="bg-foreground border border-border rounded-lg p-4" v-if="friendship_requests.length > 0">
                <h2 class="text-xl mb-6">Friendship Requests</h2>
                <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                    <div class="p-4 text-center bg-primary rounded-lg hover:bg-primary-hover" v-for="(friendshipRequest, index) in friendship_requests" :key="index">
                        <router-link :to="{ name: 'profile', params: { 'id': friendshipRequest.created_by.id } }">
                            <img :src="friendshipRequest.created_by.avatar_link"
                                class="mb-6 mx-auto w-24 h-24 rounded-full object-cover object-center">
                            <p><strong>{{friendshipRequest.created_by.name}}</strong></p>
                            <div class="mt-3 flex space-x-4 justify-around">
                                <p class="text-xs text-secondary">{{friendshipRequest.created_by.friends_count}} friends
                                </p>
                                <p class="text-xs text-secondary">{{friendshipRequest.created_by.posts_count}} posts</p>
                            </div>
                        </router-link>
                        <div class="mt-3 flex space-x-3 justify-between">
                            <button class="py-1 px-1 bg-button-primary text-white rounded-md text-xs w-full"
                                @click="handleRequest('accepted', friendshipRequest)">
                                Accept
                            </button>
                            <button class="py-1 px-1 bg-gray-600 text-white rounded-md text-xs w-full"
                                @click="handleRequest('rejected', friendshipRequest)">
                                Reject
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-foreground border border-border rounded-lg p-4" v-if="friends.length > 0">
                <h2 class="text-xl mb-6">Friendships</h2>
                <div class=" grid grid-cols-2 md:grid-cols-3 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                    <div class="p-4 text-center bg-primary rounded-lg hover:bg-primary-hover" v-for="(friend, index) in friends"  :key="index">
                        <router-link :to="{ name: 'profile', params: { 'id': friend.id } }">
                            <img :src="friend.avatar_link"
                                class="mb-6 mx-auto w-12 h-12 rounded-full object-cover object-center">
                            <p><strong>{{friend.name}}</strong></p>
                            <div class="mt-3 flex space-x-4 justify-around">
                                <p class="text-xs text-secondary">{{friend.friends_count}} friends</p>
                                <p class="text-xs text-secondary">{{friend.posts_count}} posts</p>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>

        </div>

        <!-- People you may know -->
        <div class="main-right col-span-1 space-y-4">
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
import {
  useUserStore
} from '@/stores/user';
import {
} from 'vue';
import { FriendshipRequest, User } from '@/interfaces';
export default defineComponent({
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    };
  },
  components: {
    PeopleYouMayKnow,
    Trends
  },
  data() {
    return {
      user: {} as User,
      friendship_requests: [] as FriendshipRequest[],
      friends: []
    };
  },
  methods: {
    async getFriends() {
      await axios.get(`/api/friends/${this.$route.params.id}/`).then(response => {
        this.friendship_requests = response.data.requests;
        this.friends = response.data.friends;
        this.user = response.data.user;
      }).catch(error => {
        console.log(error);
      });
    },
    async handleRequest(status: string, friendship_request: FriendshipRequest) {
      axios.post(`/api/friends/${friendship_request.created_by.id}/request/${friendship_request.id}/`, {
        status
      }).then(() => {
        this.getFriends();
        if (status === 'accepted') {
          this.user.friends_count += 1;
        }
      }).catch(error => {
        console.log(error);
      });
    },

  },
  created() {
    this.getFriends();
  }
});
</script>
<style lang=""></style>