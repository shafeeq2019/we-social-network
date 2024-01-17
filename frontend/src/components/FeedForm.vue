<template>
    <form method="post" @submit.prevent="submitForm">
        <div class="bg-white border border-gray-200 rounded-lg">
            <div class="p-4">
                <textarea class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"
                    v-model="body"></textarea>
                <div id="preview" v-if="url">
                    <img :src="url" class="w-[100px] mt-3 rounded-xl" />
                </div>
            </div>

            <div
                class="p-4 border-t border-gray-100 flex justify-between flex-col sm:flex-row md:flex-row lg:flex-row space-y-2 sm:space-y-0">
                <label for="upload" class="inline-block bg-gray-600 text-white rounded-lg cursor-pointer py-3 px-3">Attach
                    Image</label>
                <input id="upload" type="file" ref="postPhoto" accept="image/*" @change="onFileChange" hidden />
                <div class="flex justify-between flex-col sm:flex-row md:flex-row lg:flex-row space-y-2 sm:space-y-0">
                    <select id="privacy" v-model="privacy"
                        class="bg-gray-600 text-white border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 inline-block py-3 px-3">
                        <option selected value='public'>Public</option>
                        <option value="private">Private</option>
                    </select>
                    <button type="submit"
                        class="inline-block bg-purple-600 text-white rounded-lg py-3 px-6 ml-0 sm:ml-2">Post</button>
                </div>
            </div>
        </div>
    </form>
</template>
<script lang="ts">
import { PropType, defineComponent } from 'vue'
import axios from 'axios';
import { useUserStore } from '@/stores/user'
import { User, Post } from '../interfaces.ts'

export default defineComponent({
    props: {
        user: {
            type: Object as PropType<User>,
            required: false
        },
        posts: {
            type: Array as PropType<Post[]>,
            required: true
        }
    },
    setup() {
        const userStore = useUserStore();
        return {
            userStore
        }
    },
    data() {
        return {
            body: '',
            url: '',
            privacy: 'public'
        }
    },
    methods: {
        onFileChange() {
            const file = (this.$refs.postPhoto as any).files[0];
            this.url = URL.createObjectURL(file)
        },
        async submitForm() {
            axios.post("/api/post/create/", {
                body: this.body,
                image: (this.$refs.postPhoto as any).files[0]
            }, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            }).then(response => {
                this.body = '';
                (this.$refs.postPhoto as any).value = null;
                this.url = '';
                this.posts.unshift(response.data)
                this.user ? this.user.posts_count += 1 : '';
            }).catch(error => {
                console.log(error);
            })
        },
    },
})
</script>
<style></style>