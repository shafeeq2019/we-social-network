import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from "@/stores/user";
import SignupView from '../views/SignupView.vue';
import LoginView from '../views/LoginView.vue';
import FeedView from '../views/FeedView.vue';
import MessageView from '../views/MessageView.vue';
import SearchView from '../views/SearchView.vue';
import ProfileView from '../views/ProfileView.vue';
import FriendsView from '../views/FriendsView.vue';
import PostView from '../views/PostView.vue';
import TrendsView from '../views/TrendsView.vue';
import EditProfileView from '../views/EditProfileView.vue';
import EditPasswordView from '../views/EditPasswordView.vue';
import NotificationsView from '../views/NotificationsView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: FeedView,
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: {
        hideForAuth: true,
      },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        hideForAuth: true,
      },
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/messages/:user_id?',
      name: 'messages',
      component: MessageView,
      props: true,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/trends/:hashtag',
      name: 'trendsview',
      component: TrendsView,
      props: true,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView,
      meta: {
        requiresAuth: true,
      },
    }
  ]
});

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!userStore.user.isAuthenticated) {
      next({ name: 'login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  }

  if (to.matched.some((record) => record.meta.hideForAuth)) {
    if (userStore.user.isAuthenticated) {
      next({ path: "/feed" });
    } else {
      next();
    }
  }

});

export default router;
