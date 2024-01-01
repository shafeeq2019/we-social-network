<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-3 space-y-4">
            <form method="post" @submit.prevent="submitForm">
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
            <FeedItem v-for="post in posts" :post="post" :key="post.id" />
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
import FeedItem from '../components/FeedItem.vue'

export default {
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },
    data() {
        return {
            posts: [],
            body: ''
        }
    },
    methods: {
        async getFeeds() {
            await axios.get('/api/post').then(response => {
                this.posts = response.data.data;
            }).catch(error => {
                console.log(error);
            })
        },
        async submitForm() {
            axios.post("/api/post/create/", {
                "body": this.body
            }).then(async response => {
                this.body = '';
                //this.posts = [response.data, ...this.posts];
                await this.getFeeds()
            }).catch(error => {
                console.log(error);
            })
        }
    },
    mounted() {
        this.getFeeds();
    }
};
</script>
<style lang=""></style>