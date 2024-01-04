<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-3 space-y-4">
            <FeedItem :post="post" v-if="post.created_by" />
            <div class="p-4 mx-6 bg-white border border-gray-200 rounded-lg" v-for="comment in post.comments" :key="comment.id">
                <CommentItem :comment="comment" />
            </div>

            <div class="bg-white border border-gray-200 rounded-lg" >
                <form method="post" @submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking?"
                            v-model="commentText"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button type="submit"
                            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>
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
import FeedItem from '../components/FeedItem.vue'
import CommentItem from '../components/CommentItem.vue'

export default {
    async beforeRouteUpdate(to, from) {
        // react to route changes...
        await this.getPost(to.params.id);
    },
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        CommentItem
    },
    data() {
        return {
            post: {
                comments: []
            },
            commentText: ''
        }
    },
    methods: {
        async getPost() {
            await axios.get(`/api/post/${this.$route.params.id}/detail/`).then(response => {
                this.post = response.data.post;
            }).catch(error => {
                console.log(error);
            })
        },
        async submitForm() {
            axios.post(`/api/post/${this.$route.params.id}/comment/`, {
                "comment": this.commentText
            }).then(async response => {
                this.commentText = '';
                //this.post.comments = [this.post.comments, ...this.commentText];
                await this.getPost()
            }).catch(error => {
                console.log(error);
            })
        }
    },
    created() {
        this.getPost()
    }
};
</script>
<style lang=""></style>