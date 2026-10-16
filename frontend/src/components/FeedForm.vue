<template>
  <form method="post" @submit.prevent="submitForm"
        :class="['surface transition-shadow duration-200', focused ? 'shadow-lift ring-1 ring-primary/20' : '']"
        aria-label="Create a post">
    <div class="flex gap-3 px-5 pt-5">
      <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" class="hidden sm:inline-flex" />
      <div class="min-w-0 flex-1">
        <label :for="textareaId" class="sr-only">What's on your mind?</label>
        <textarea :id="textareaId" ref="textarea" v-model="body" rows="2"
                  class="block max-h-72 min-h-[56px] w-full resize-none bg-transparent pt-2 text-[17px] leading-relaxed placeholder:text-muted-foreground/80 focus-visible:outline-none focus-visible:ring-0 focus-visible:ring-offset-0"
                  :placeholder="placeholder" @focus="focused = true" @blur="focused = false" @input="autoGrow"
                  @keydown.meta.enter.prevent="submitForm" @keydown.ctrl.enter.prevent="submitForm"></textarea>

        <div v-if="url" class="relative mt-3 inline-block animate-in fade-in zoom-in-95">
          <img :src="url" alt="Selected image preview" class="max-h-72 rounded-2xl border border-border/60 object-cover" />
          <button type="button" class="absolute right-2 top-2 flex h-8 w-8 items-center justify-center rounded-full bg-foreground/75 text-background backdrop-blur transition hover:bg-foreground"
                  aria-label="Remove image" @click="removeImage">
            <X class="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>

    <div class="mt-3 flex flex-wrap items-center gap-1.5 border-t border-border/60 px-3 py-3 sm:px-4">
      <label :for="fileId"
             class="inline-flex h-10 cursor-pointer items-center gap-2 rounded-full px-3 text-sm font-semibold text-muted-foreground transition-colors hover:bg-primary/10 hover:text-primary-soft-foreground focus-within:ring-2 focus-within:ring-ring dark:hover:text-primary">
        <ImagePlus class="h-5 w-5" aria-hidden="true" />
        <span class="sr-only sm:not-sr-only">Photo</span>
        <input :id="fileId" type="file" ref="postPhoto" accept="image/*" class="sr-only" @change="onFileChange">
      </label>

      <div role="radiogroup" aria-label="Who can see this post" class="inline-flex h-10 items-center rounded-full bg-muted p-1">
        <button v-for="option in privacyOptions" :key="String(option.value)" type="button" role="radio"
                :aria-checked="is_private === option.value"
                :class="['inline-flex h-8 items-center gap-1.5 rounded-full px-3 text-[13px] font-semibold transition-all',
                         is_private === option.value ? 'bg-card text-foreground shadow-soft' : 'text-muted-foreground hover:text-foreground']"
                @click="is_private = option.value">
          <component :is="option.icon" class="h-3.5 w-3.5" aria-hidden="true" />
          {{ option.label }}
        </button>
      </div>

      <btn class="ml-auto px-5 sm:px-6" type="submit" :loading="submitting" :disabled="!canSubmit">Post</btn>
    </div>
  </form>
</template>

<script lang="ts">
import { PropType, defineComponent } from 'vue';
import { Globe2, ImagePlus, Lock, X } from 'lucide-vue-next';
import btn from './ui/Button.vue';
import Avatar from './ui/Avatar.vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { User, Post } from '../interfaces.ts';

let uid = 0;

export default defineComponent({
  components: { btn, Avatar, ImagePlus, X },
  props: {
    user: {
      type: Object as PropType<User | null>,
      required: false
    },
    posts: {
      type: Array as PropType<Post[]>,
      required: true
    }
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    uid += 1;
    return {
      userStore,
      toastStore,
      textareaId: `post-body-${uid}`,
      fileId: `post-image-${uid}`,
      privacyOptions: [
        { value: false, label: 'Public', icon: Globe2 },
        { value: true, label: 'Only me', icon: Lock },
      ]
    };
  },
  data() {
    return {
      body: '',
      url: '',
      is_private: false,
      focused: false,
      submitting: false
    };
  },
  computed: {
    canSubmit(): boolean {
      return this.body.trim().length > 0 || !!this.url;
    },
    placeholder(): string {
      const firstName = (this.userStore.user.name || '').split(' ')[0];
      return firstName ? `What's new, ${firstName}?` : 'What\'s on your mind?';
    }
  },
  methods: {
    fileInput(): HTMLInputElement {
      return this.$refs.postPhoto as HTMLInputElement;
    },
    onFileChange() {
      const file = this.fileInput().files?.[0];
      if (this.url) {
        URL.revokeObjectURL(this.url);
      }
      this.url = file ? URL.createObjectURL(file) : '';
    },
    removeImage() {
      URL.revokeObjectURL(this.url);
      this.url = '';
      this.fileInput().value = '';
    },
    autoGrow() {
      const el = this.$refs.textarea as HTMLTextAreaElement;
      el.style.height = 'auto';
      el.style.height = `${el.scrollHeight}px`;
    },
    async submitForm() {
      if (!this.canSubmit || this.submitting) {
        return;
      }
      const imageInput = this.fileInput();
      this.submitting = true;
      axios.post('/api/post/create/', {
        body: this.body,
        image: imageInput.files![0],
        is_private: this.is_private
      }, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        this.body = '';
        this.is_private = false;
        imageInput.value = '';
        this.url = '';
        (this.$refs.textarea as HTMLTextAreaElement).style.height = '';
        /* eslint-disable */
        this.posts.unshift(response.data);
        this.user ? this.user.posts_count += 1 : '';
        /* eslint-enable */
        this.toastStore.showToast(3000, 'Your post is live', 'bg-emerald-500');
      }).catch(error => {
        console.log(error);
        this.toastStore.showToast(5000, 'Your post could not be published. Please try again.', 'bg-red-300');
      }).finally(() => {
        this.submitting = false;
      });
    },
  },
});
</script>
