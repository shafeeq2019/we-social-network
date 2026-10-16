<template>
  <AuthLayout title="Welcome back" subtitle="Log in to catch up with your friends.">
    <form class="space-y-5" novalidate @submit.prevent="submitForm">
      <div>
        <label for="login-email" class="field-label">E-mail</label>
        <input id="login-email" type="email" autocomplete="email" placeholder="you@example.com"
               class="field h-12" v-model="form.email">
      </div>
      <div>
        <label for="login-password" class="field-label">Password</label>
        <div class="relative">
          <input id="login-password" :type="showPassword ? 'text' : 'password'" autocomplete="current-password"
                 placeholder="Your password" class="field h-12 pr-12" v-model="form.password">
          <button type="button" class="icon-btn absolute right-1 top-1/2 -translate-y-1/2"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'" :aria-pressed="showPassword"
                  @click="showPassword = !showPassword">
            <EyeOff v-if="showPassword" class="h-4 w-4" aria-hidden="true" />
            <Eye v-else class="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </div>

      <FormErrors :errors="errors" />

      <btn size="lg" class="w-full" type="submit" :loading="submitting">Log in</btn>
    </form>

    <template #footer>
      New to We?
      <RouterLink :to="{ name: 'signup' }" class="font-semibold text-foreground underline-offset-2 hover:underline">Create an account</RouterLink>
    </template>
  </AuthLayout>
</template>

<script lang="ts">
import axios from 'axios';
import { Eye, EyeOff } from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import { defineComponent } from 'vue';
import btn from '@/components/ui/Button.vue';
import FormErrors from '@/components/ui/FormErrors.vue';
import AuthLayout from '@/components/layout/AuthLayout.vue';
export default defineComponent({
  components: { btn, FormErrors, AuthLayout, Eye, EyeOff },
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    };
  },
  data() {
    return {
      form: {
        email: '' as string,
        password: '' as string,

      },
      errors: [] as string[],
      submitting: false,
      showPassword: false
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing');
      }

      if (this.form.password === '') {
        this.errors.push('Your password is missing');
      }

      if (this.errors.length === 0) {
        this.submitting = true;
        await axios.post('/api/login/', this.form)
          .then(async response => {
            this.userStore.setToken(response.data);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;

            await axios.get('/api/me/')
              .then(response => {
                this.userStore.setUserInfo(response.data);
                this.$router.push(this.$route.query.redirect as string || '/feed');
              }).catch(error => {
                throw error;
              });
          })
          .catch(error => {
            console.log('error', error);
            this.errors.push('The email or password is incorrect! Or the user is not activated!');
          })
          .finally(() => {
            this.submitting = false;
          });

      }
    }
  }
});
</script>
