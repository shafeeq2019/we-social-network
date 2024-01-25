<template lang="">
    <div class="p-4 bg-white border border-gray-200 rounded-lg">

        <div class="mb-6 flex items-center justify-between">
            <router-link :to="{ name: 'profile', params: { 'id': post.created_by.id } }">
                <div class="flex items-center space-x-3">
                    <img :src="post.created_by.avatar_link ? post.created_by.avatar_link : user.avatar_link"
                        class="w-[40px] h-[39px] rounded-full">

                    <p><strong>{{post.created_by.name ? post.created_by.name : user.name }}</strong></p>
                </div>
            </router-link>

            <p class="text-gray-600">{{ /^0\s+minutes$/.test(post.created_ago) ? 'Just now' : post.created_ago}}</p>
        </div>

        <p v-html="formatHashtags(post.body)"> </p>

        <img :src="post.post_attachments[0].image_link" :key="post.post_attachments[0].id"
            class="w-full rounded-lg mt-4" v-if="post.post_attachments.length > 0">

        <div class="my-6 flex justify-between">
            <div class="flex space-x-6">
                <div class="flex items-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" :fill="post.post_liked ? 'red' : 'none'" viewBox="0 0 24 24"
                        stroke-width="1.5" @click="likePost" :stroke="post.post_liked ? 'red' : 'currentColor'"
                        class="w-6 h-6 cursor-pointer">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
                        </path>
                    </svg>

                    <span class="text-gray-500 text-xs">{{post.likes_count}}</span>
                </div>

                <div class="flex items-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6 cursor-pointer">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                        </path>
                    </svg>

                    <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">
                        {{ post.comments_count }} comments</RouterLink>
                </div>

                <div class="flex items-center space-x-2 text-gray-500" v-if="post.is_private">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>

                    <span class="text-gray-500 text-xs">private</span>
                </div>

            </div>

            <div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                    </path>
                </svg>
            </div>

        </div>
    </div>
</template>
<script lang="ts">
import {
    defineComponent
} from 'vue'
import axios from 'axios';
import {
    Post,
    User
} from '../interfaces.ts'
import type {
    PropType
} from 'vue'
export default defineComponent({
    setup() { },
    props: {
        post: {
            type: Object as PropType<Post>,
            required: true
        },
        user: Object as PropType<User>
    },
    methods: {
        likePost() {
            axios.post(`/api/post/${this.post.id}/like/`).then(response => {
                if (response.data.message == 'post liked successfully') {
                    this.post.likes_count += 1;
                    this.post.post_liked = true
                } else {
                    this.post.likes_count -= 1;
                    this.post.post_liked = false
                }
            }).catch(e => {
                console.log(e)
            })
        },
        formatHashtags(text: string): string {
            const escapeHTML = (text: string) => text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const escapedText = escapeHTML(text);
            return escapedText.replace(/\B#(\w+)/g,
                '<a class="text-blue-700" href="/trends/$1">#$1</a>');
        }
    },
    created() {
    }
})
</script>
<style lang="">

</style>