<template>
  <PageLayout no-aside>
    <PageHeader eyebrow="Settings" title="Change password" description="Use at least 8 characters that you don't use elsewhere." />
    <SettingsNav />

    <form class="surface space-y-5 p-5 sm:p-7" novalidate v-on:submit.prevent="submitForm">
      <div>
        <label for="old-password" class="field-label">Current password</label>
        <input id="old-password" type="password" v-model="form.old_password" autocomplete="current-password"
               placeholder="Your current password" class="field h-12">
      </div>
      <div class="grid gap-5 sm:grid-cols-2">
        <div>
          <label for="new-password1" class="field-label">New password</label>
          <input id="new-password1" type="password" v-model="form.new_password1" autocomplete="new-password"
                 placeholder="New password" class="field h-12">
        </div>
        <div>
          <label for="new-password2" class="field-label">Repeat new password</label>
          <input id="new-password2" type="password" v-model="form.new_password2" autocomplete="new-password"
                 placeholder="Repeat it" class="field h-12">
        </div>
      </div>

      <FormErrors :errors="errors" />

      <div class="flex flex-col-reverse gap-2 border-t border-border/60 pt-5 sm:flex-row sm:justify-end">
        <btn variant="ghost" type="button" @click="$router.back()">Cancel</btn>
        <btn type="submit" :loading="submitting">Update password</btn>
      </div>
    </form>
  </PageLayout>
</template>

<script lang="ts">
/**
TODOS:
- Error handling for Sing up and change password
*/
import { defineComponent } from 'vue';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import btn from '@/components/ui/Button.vue';
import FormErrors from '@/components/ui/FormErrors.vue';
import PageLayout from '@/components/layout/PageLayout.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import SettingsNav from '@/components/layout/SettingsNav.vue';

export default defineComponent({
  components: { btn, FormErrors, PageLayout, PageHeader, SettingsNav },
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();

    return {
      toastStore,
      userStore
    };
  },
  data() {
    return {
      form: {
        old_password: '' as string,
        new_password1: '' as string,
        new_password2: '' as string
      },
      errors: [] as string[],
      submitting: false
    };
  },
  methods: {
    submitForm() {
      this.errors = [];
      if (this.form.new_password1 !== this.form.new_password2) {
        this.errors.push('The password does not match');
      }

      if (this.errors.length === 0) {
        this.submitting = true;
        axios
          .post('/api/editpassword/', this.form)
          .then(response => {
            if (response.data.message === 'success') {
              this.toastStore.showToast(5000, 'Your password was successfully updated!', 'bg-emerald-500');
              this.$router.push(`/profile/${this.userStore.user.id}`);
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

  }
});
</script>
