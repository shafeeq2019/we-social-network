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

            <div class="p-4 border-t border-gray-100 flex justify-between">
                <label for="upload" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg cursor-pointer">Attach
                    Image</label>
                <input id="upload" type="file" ref="postPhoto" accept="image/*" @change="onFileChange" hidden />
                <button type="submit" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
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
            url: ''
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