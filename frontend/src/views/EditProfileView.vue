<template>
  <PageLayout no-aside>
    <PageHeader eyebrow="Settings" title="Edit profile" description="Change how you appear to others on We." />
    <SettingsNav />

    <form class="surface space-y-6 p-5 sm:p-7" novalidate v-on:submit.prevent="submitForm">
      <div class="flex flex-col items-start gap-5 sm:flex-row sm:items-center">
        <Avatar :src="avatarPreview || userStore.user.avatar_link" :name="form.name" size="xl" />
        <div>
          <p class="field-label mb-1">Profile picture</p>
          <p class="mb-3 text-sm text-muted-foreground">A square image of at least 400 × 400 px works best.</p>
          <label for="file-input"
                 class="inline-flex h-10 cursor-pointer items-center gap-2 rounded-full border border-border bg-card px-4 text-sm font-semibold transition hover:bg-muted focus-within:ring-2 focus-within:ring-ring">
            <Camera class="h-4 w-4" aria-hidden="true" /> {{ avatarPreview ? 'Choose another' : 'Upload new picture' }}
            <input class="sr-only" type="file" accept="image/*" ref="file" id="file-input" @change="onAvatarChange">
          </label>
        </div>
      </div>

      <div class="grid gap-5 sm:grid-cols-2">
        <div>
          <label for="profile-name" class="field-label">Name</label>
          <input id="profile-name" type="text" v-model="form.name" autocomplete="name" placeholder="Your full name" class="field h-12">
        </div>
        <div>
          <label for="profile-email" class="field-label">E-mail</label>
          <input id="profile-email" type="email" v-model="form.email" autocomplete="email" placeholder="you@example.com" class="field h-12">
        </div>
      </div>

      <FormErrors :errors="errors" />

      <div class="flex flex-col-reverse gap-2 border-t border-border/60 pt-5 sm:flex-row sm:justify-end">
        <btn variant="ghost" type="button" @click="$router.back()">Cancel</btn>
        <btn type="submit" :loading="submitting">Save changes</btn>
      </div>
    </form>
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { Camera } from 'lucide-vue-next';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import btn from '@/components/ui/Button.vue';
import Avatar from '@/components/ui/Avatar.vue';
import FormErrors from '@/components/ui/FormErrors.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import SettingsNav from '@/components/layout/SettingsNav.vue';

export default defineComponent({
  components: { btn, Avatar, FormErrors, PageLayout, PageHeader, SettingsNav, Camera },
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();
    return {
      toastStore,
      userStore,
    };
  },
  data() {
    return {
      form: {
        name: '',
        email: ''
      },
      errors: [] as string[],
      avatarPreview: '',
      submitting: false
    };
  },
  methods: {
    onAvatarChange() {
      const file = (this.$refs.file as HTMLInputElement).files?.[0];
      if (this.avatarPreview) {
        URL.revokeObjectURL(this.avatarPreview);
      }
      this.avatarPreview = file ? URL.createObjectURL(file) : '';
    },
    submitForm() {
      this.errors = [];

      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing');
      }

      if (this.form.name === '') {
        this.errors.push('Your name is missing');
      }
      if (this.errors.length === 0) {
        const formData = new FormData();
        const avatar = (this.$refs.file as HTMLInputElement).files?.[0];
        if (avatar) {
          formData.append('avatar', avatar);
        }
        formData.append('email', this.form.email);
        formData.append('name', this.form.name);
        this.submitting = true;
        axios
          .post('/api/editprofile/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(response => {
            if (response.data.message === 'success') {
              this.toastStore.showToast(5000, 'The information was saved.', 'bg-emerald-500');
              this.userStore.setUserInfo(response.data.updated_user);
              this.form.email = this.userStore.user.email;
              this.form.name = this.userStore.user.name;
              this.$router.back();
            } else {
              const data = JSON.parse(response.data.message);
              for (const key in data) {
                this.errors.push(data[key][0].message);
              }
              this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300');
            }
          })
          .catch(error => {
            console.log('error', error);
            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300');
          })
          .finally(() => {
            this.submitting = false;
          });
      }
    }

  },
  created() {
    this.form.name = this.userStore.user.name;
    this.form.email = this.userStore.user.email;

  }
});
</script>
