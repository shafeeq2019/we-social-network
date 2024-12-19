<template>
  <form method="post" @submit.prevent="submitForm">
    <div class="bg-foreground border border-border rounded-lg text-primary">
      <div class="p-4">
        <textarea class="p-4 w-full border-border rounded-lg bg-background text-primary dark:focus:outline-none" placeholder="What are you thinking about?"
                  v-model="body">
                </textarea>
        <div id="preview" v-if="url">
          <img :src="url" class="w-[100px] mt-3 rounded-xl" />
        </div>
      </div>

      <div class="p-4 border-t border-border flex justify-between flex-col sm:flex-row space-y-2 sm:space-y-0">
        <label for="upload-image"
               class="inline-block bg-button-secondary text-white rounded-lg cursor-pointer p-1 sm:py-3 sm:px-6 text-center">Attach
          Image</label>
        <input id="upload-image" type="file" ref="postPhoto" accept="image/*" @input="onFileChange" hidden>
        <div class="flex justify-between flex-col sm:flex-row md:flex-row lg:flex-row space-y-2 sm:space-y-0">
          <!-- <select id="privacy" v-model="is_private"
                        class="bg-gray-600 text-white border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 inline-block py-3 px-3 cursor-pointer">
                        <option selected value=false>Public</option>
                        <option value=true>Private</option>
                    </select>  -->
          <button type="submit"
                  class="inline-block bg-button-primary text-white rounded-lg p-1 sm:py-3 sm:px-6 ml-0 sm:ml-2">Post</button>
        </div>
      </div>
    </div>
  </form>
</template>
<script lang="ts">
import { PropType, defineComponent } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { User, Post } from '../interfaces.ts';

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
    };
  },
  data() {
    return {
      body: '',
      url: '',
      is_private: false
    };
  },
  methods: {
    onFileChange() {
      const imageInput = document.getElementById("upload-image")! as HTMLInputElement;
      this.url = URL.createObjectURL(imageInput.files![0]);
    },
    async submitForm() {
      const imageInput = document.getElementById("upload-image")! as HTMLInputElement;
      axios.post("/api/post/create/", {
        body: this.body,
        image: imageInput.files![0],
        is_private: this.is_private
      }, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }).then(response => {
        this.body = '';
        this.is_private = false;
        imageInput.value = "";
        this.url = '';
        /* eslint-disable */
        this.posts.unshift(response.data);
        this.user ? this.user.posts_count += 1 : '';
      }).catch(error => {
        console.log(error);
      });
    },
  },
});
</script>
<style></style>