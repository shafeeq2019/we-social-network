<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- User on the left -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="flex items-center justify-center">
                    <img src="https://i.pravatar.cc/200?img=57" class="mb-6 rounded-full" />
                </div>

                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <router-link :to="{name:'friends', params:{id: user.id} }" class="text-xs text-gray-500">{{user.friends_count}} friends</router-link>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>

                <div class="mt-6" v-if="user.id != userStore.user.id">
                    <button class="inline-block py-3 px-3 bg-purple-600 text-white rounded-lg text-xs" @click="sendFriendshipRequest"> Send friendship
                        request</button>
                </div>
            </div>
        </div>
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-2 space-y-4">
            <form method="post" @submit.prevent="submitForm" v-if="userStore.user.id == user.id">
                <div class="bg-white border border-gray-200 rounded-lg">
                    <div class="p-4">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"
                            v-model="body"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach
                            image</button>
                        <button type="submit"
                            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </div>
            </form>

            <FeedItem v-for="post in posts" :user="user" :post="post" :key="post.id" />
        </div>

        <!-- People you may know -->
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>

    </div>
</template>
<script>
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import {
    useUserStore
} from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'
import {
    ref,
    watch,
    onMounted
} from 'vue';
export default {
    async beforeRouteUpdate(to, from) {
        // react to route changes...
        await this.getFeeds(to.params.id);
    },
    setup() {
        const userStore = useUserStore();
        return {
            userStore
        }
    },
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },
    data() {
        return {
            posts: [],
            user: {},
            body: ''
        }
    },
    methods: {
        async getFeeds(userId) {
            await axios.get(`/api/post/profile/${userId}/`).then(response => {
                this.posts = response.data.posts;
                this.user = response.data.user
            }).catch(error => {
                console.log(error);
            })
        },
        async submitForm() {
            axios.post("/api/post/create/", {
                "body": this.body
            }).then(response => {
                this.body = '';
                this.posts = [response.data, ...this.posts];
            }).catch(error => {
                console.log(error);
            })
        },
        async sendFriendshipRequest() {
            axios.post(`/api/friends/request/${this.$route.params.id}/`).then(response => {
                console.log(response);
            }).catch(error => {
                console.log(error);
            })
        }
    },
    created() {
        this.getFeeds(this.$route.params.id);
    }
};
</script>
<style lang=""></style>