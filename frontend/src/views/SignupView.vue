<template>
  <AuthLayout title="Join We" subtitle="Create your free account in less than a minute.">
    <div v-if="registered" class="surface p-6 text-center animate-fade-up" role="status">
      <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-success/15 text-success">
        <MailCheck class="h-6 w-6" aria-hidden="true" />
      </div>
      <h2 class="text-lg font-bold">Check your inbox</h2>
      <p class="mt-1 text-sm text-muted-foreground">
        We sent you an activation link. Activate your account, then log in.
      </p>
      <RouterLink :to="{ name: 'login' }"
                  class="mt-5 inline-flex h-10 items-center rounded-full bg-foreground px-5 text-sm font-semibold text-background transition hover:bg-foreground/85">
        Go to log in
      </RouterLink>
    </div>

    <form v-else class="space-y-5" novalidate v-on:submit.prevent="submitForm">
      <div>
        <label for="signup-name" class="field-label">Name</label>
        <input id="signup-name" type="text" v-model="form.name" autocomplete="name" placeholder="Your full name" class="field h-12">
      </div>
      <div>
        <label for="signup-email" class="field-label">E-mail</label>
        <input id="signup-email" type="email" v-model="form.email" autocomplete="email" placeholder="you@example.com" class="field h-12">
      </div>
      <div class="grid gap-5 sm:grid-cols-2">
        <div>
          <label for="signup-password1" class="field-label">Password</label>
          <input id="signup-password1" type="password" v-model="form.password1" autocomplete="new-password"
                 placeholder="Create a password" class="field h-12">
        </div>
        <div>
          <label for="signup-password2" class="field-label">Repeat password</label>
          <input id="signup-password2" type="password" v-model="form.password2" autocomplete="new-password"
                 placeholder="Repeat it" class="field h-12">
        </div>
      </div>

      <FormErrors :errors="errors" />

      <btn size="lg" class="w-full" type="submit" :loading="submitting">Create account</btn>
    </form>

    <template #footer>
      Already have an account?
      <RouterLink :to="{ name: 'login' }" class="font-semibold text-foreground underline-offset-2 hover:underline">Log in</RouterLink>
    </template>
  </AuthLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { MailCheck } from 'lucide-vue-next';
import { useToastStore } from '@/stores/toast';
import btn from '@/components/ui/Button.vue';
import FormErrors from '@/components/ui/FormErrors.vue';
import AuthLayout from '@/components/layout/AuthLayout.vue';

export default defineComponent({
  components: { btn, FormErrors, AuthLayout, MailCheck },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore
    };
  },

  data() {
    return {
      form: {
        email: '',
        name: '',
        password1: '',
        password2: ''
      },
      errors: [] as string[],
      submitting: false,
      registered: false
    };
  },

  methods: {
    submitForm() {
      this.errors = [];

      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing');
      }

      if (this.form.name === '') {
        this.errors.push('Your name is missing');
      }

      if (this.form.password1 === '') {
        this.errors.push('Your password is missing');
      }

      if (this.form.password1 !== this.form.password2) {
        this.errors.push('The password does not match');
      }

      if (this.errors.length === 0) {
        this.submitting = true;
        axios
          .post('/api/signup/', this.form)
          .then(response => {
            if (response.data.message === 'success') {
              this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link.', 'bg-emerald-500');

              this.form.email = '';
              this.form.name = '';
              this.form.password1 = '';
              this.form.password2 = '';
              this.registered = true;
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
