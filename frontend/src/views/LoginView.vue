<template lang="">
  <div class="mx-auto grid grid-cols-2 gap-4  text-primary">
    <div class="main-left col-span-2 md:col-span-1">
      <div class="p-12 bg-foreground border border-border rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-secondary">
          <b>We</b> is a social network for sharing news and making new friendships. Log in or join now - it's free
        </p>
        <p class="font-bold">
          Don't have an account? <RouterLink :to="{'name': 'signup'}" class="underline">Click here</RouterLink> to
          create one!
        </p>
      </div>
    </div>
    <div class="main-right col-span-2 md:col-span-1 text-primary">
      <div class="p-12 bg-foreground border border-border rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>E-mail</label><br>
            <input type="email" placeholder="Your e-mail address"
                   class="w-full mt-2 py-4 px-6 border border-border rounded-lg bg-background" v-model="form.email">
          </div>
          <div>
            <label>Password</label><br>
            <input type="password" placeholder="Your password"
                   class="w-full mt-2 py-4 px-6 border border-border rounded-lg bg-background" v-model="form.password">
          </div>
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>
          <div class="flex justify-end">
            <btn size="big" class="w-full sm:w-auto">Log in</btn>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { defineComponent } from 'vue';
import btn from '@/components/ui/Button.vue';
export default defineComponent({
  components: { btn },
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    };
  },
  data() {
    return {
      form: {
        email: "" as string,
        password: "" as string,

      },
      errors: [] as string[]
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
        await axios.post('/api/login/', this.form)
          .then(async response => {
            this.userStore.setToken(response.data);
            axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;

            await axios.get("/api/me/")
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
          });

      }
    }
  }
});
</script>
<style lang="">

</style>
