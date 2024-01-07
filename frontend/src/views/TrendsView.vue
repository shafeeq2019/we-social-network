<template lang="">
    <div class="mb-4 max-w-7xl mx-auto">
        <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-md">
            <h2 class="text-xl">Trend: #{{hashtag}}</h2>
        </div>
    </div>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-3 space-y-4">
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
        props: ['hashtag'],
        async beforeRouteUpdate(to, from) {
            await this.getFeeds(to.params.hashtag);
        },
        components: {
            PeopleYouMayKnow,
            Trends,
            FeedItem
        },
        data() {
            return {
                posts: []
            }
        },
        methods: {
            async getFeeds(hashtag) {
                await axios.get(`/api/post?trend=${hashtag}`).then(response => {
                    this.posts = response.data.data;
                }).catch(error => {
                    console.log(error);
                })
            },
        },
        created() {
            this.getFeeds(this.hashtag)
        }
    };
</script>
<style lang=""></style>