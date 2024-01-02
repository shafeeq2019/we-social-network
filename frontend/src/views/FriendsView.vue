<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-4 xl:grid-cols-4 gap-4">
        <!-- User on the left -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="flex items-center justify-center">
                    <img src="https://i.pravatar.cc/200?img=57" class="mb-6 rounded-full" />
                </div>

                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">182 friends</p>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>
            </div>
        </div>

        <div class="main-center lg:col-span-2 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg p-4" v-if="friendshipRequests.length > 0">
                <h2 class="text-xl mb-6">Friendship Requests</h2>
                <div class=" grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                    <div class="p-4 text-center bg-gray-100 rounded-lg hover:bg-gray-200" v-for="friendshipRequest in friendshipRequests">
                        <router-link :to="{ name: 'profile', params: { 'id': friendshipRequest.created_by.id } }">
                            <img src="https://i.pravatar.cc/300?img=70" class="mb-6 mx-auto rounded-full">
                            <p><strong>{{friendshipRequest.created_by.name}}</strong></p>
                            <div class="mt-6 flex space-x-8 justify-around">
                                <p class="text-xs text-gray-500">182 friends</p>
                                <p class="text-xs text-gray-500">120 posts</p>
                            </div>
                        </router-link>
                        <div class="mt-6 space-y-2 grid grid-rows-2">
                            <div row-span-1>
                                <button class="py-1 px-1 bg-purple-600 text-white rounded-md text-xs w-full ">
                                    Accept
                                </button>
                            </div>
                            <div row-span-1>
                                <button class="py-1 px-1 bg-gray-600 text-white rounded-md text-xs w-full row-span-1">
                                    Reject
                                </button>
                            </div>
                        </div>
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
        },
        setup() {
            const userStore = useUserStore();
            return {
                userStore
            }
        },
        components: {
            PeopleYouMayKnow,
            Trends
        },
        data() {
            return {
                user: {},
                friendshipRequests: [],
                friends: []
            }
        },
        methods: {
            async getFriends(userId) {
                await axios.get(`/api/friends/`).then(response => {
                    console.log(response)
                    this.friendshipRequests = response.data.requests;
                    this.friends = response.data.friends;
                    this.user = response.data.user
                }).catch(error => {
                    console.log(error);
                })
            },
        },
        created() {
            this.getFriends()
        }
    };
</script>
<style lang=""></style>