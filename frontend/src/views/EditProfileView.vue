<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left col-span-1">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Edit profile</h1>
                <p class="mb-6 text-gray-500">
                    Here you can change your name, your email, and your avatar
                </p>
                <router-link to="/profile/edit/password" class="underline"> Edit password</router-link>
            </div>
        </div>

        <div class="main-right col-span-1">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your full name"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    <div>
                        <label class="" for="file-input">Avatar</label>
                        <input
                            class="block w-full text-gray-900 border border-gray-200 rounded-lg cursor-pointer mt-2 py-4 px-6"
                            type="file" ref="file" id="file-input">
                    </div>
                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>
                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'
import { mapState } from 'pinia'

export default defineComponent({
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()
        return {
            toastStore,
            userStore,
        }
    },
    data() {
        return {
            form: {
                name: "",
                email: ""
            },
            errors: [] as string[],
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }
            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append("avatar", (this.$refs.file as any).files[0])
                formData.append("email", this.form.email)
                formData.append("name", this.form.name)
                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data"
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The information was saved.', 'bg-emerald-500')
                            this.userStore.setUserInfo(response.data.updated_user);
                            this.form.email = this.userStore.user.email
                            this.form.name = this.userStore.user.name
                            this.$router.back()
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data) {
                                this.errors.push(data[key][0].message)
                            }
                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }

    },
    created() {
        this.form.name = this.userStore.user.name;
        this.form.email = this.userStore.user.email;

    }
}) 
</script>
<style></style>