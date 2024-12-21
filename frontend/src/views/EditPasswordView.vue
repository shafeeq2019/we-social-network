/**
TODOS:
- Error handling for Sing up and change password
*/
<template>
  <div class="grid grid-cols-2 gap-4 text-primary">
    <div class="main-left col-span-2 md:col-span-1">
      <div class="p-12 bg-foreground border border-border rounded-lg">
        <h1 class="mb-6 text-2xl">Edit password</h1>
        <p class="mb-6 text-secondary">
          Here you can change your password
        </p>
      </div>
    </div>
    <div class="main-right col-span-2 md:col-span-1">
      <div class="p-12 bg-foreground border border-border rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>Old password</label><br>
            <input type="password" v-model="form.old_password" placeholder="Your old password"
                   class="w-full mt-2 py-4 px-6 border border-border rounded-lg bg-background">
          </div>
          <div>
            <label>New password</label><br>
            <input type="password" v-model="form.new_password1" placeholder="Enter your new password"
                   class="w-full mt-2 py-4 px-6 border border-border rounded-lg bg-background">
          </div>
          <div>
            <label>Repeat new password</label><br>
            <input type="password" v-model="form.new_password2" placeholder="Repeat your new password"
                   class="w-full mt-2 py-4 px-6 border border-border rounded-lg bg-background">
          </div>
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>
          <div class="flex justify-end">
            <btn size="big" variant="primary">Save changes</btn>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import btn from '@/components/ui/Button.vue';

export default defineComponent({
  components: { btn },
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
      errors: [] as string[]
    };
  },
  methods: {
    submitForm() {
      if (this.form.new_password1 !== this.form.new_password2) {
        this.errors.push('The password does not match');
      }

      if (this.errors.length === 0) {
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
          });
      }
    }

  }
});
</script>
