import { createRouter, createWebHistory } from 'vue-router';
import { getAuth } from 'firebase/auth'; // Firebase Auth import

// Import your components
import Menu from '../views/Menu.vue';
import Customize from '../views/Customize.vue';
import LogIn from '../views/LogIn.vue';
import SignUp from '../views/SignUp.vue';
import WaitingPage from '../views/WaitingPage.vue';
import UserProfile from '../views/UserProfile.vue';
import Recommend from '../views/Recommend.vue';
import MyMenu from '../views/MyMenu.vue';
import ControlPi from '@/views/ControlPi.vue';
import DonePage from '../views/DonePage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:catchAll(.*)',
      redirect: '/login',
    },
    {
      path: '/menu',
      name: 'Menu',
      component: Menu,
      meta: { requiresAuth: true },
    },
    {
      path: '/customize/:id/:img',
      name: 'Customize',
      component: Customize,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LogIn,
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp,
    },
    {
      path: '/WaitingPage',
      name: 'WaitingPage',
      component: WaitingPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/DonePage',
      name: 'DonePage',
      component: DonePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/UserProfile',
      name: 'UserProfile',
      component: UserProfile,
      meta: { requiresAuth: true },
    },
    {
      path: '/Recommend',
      name: 'Recommend',
      component: Recommend,
      meta: { requiresAuth: true },
    },
    {
      path: '/mymenu',
      name: 'MyMenu',
      component: MyMenu,
      meta: { requiresAuth: true },
    },
    {
      path: '/controlpi',
      name: 'ControlPi',
      component: ControlPi,
      meta: { requiresAuth: true },
    },
  ],
});

// Add a global navigation guard (to -> destination, from -> source, next -> redirect to where)
router.beforeEach((to, from, next) => {
  const auth = getAuth();
  const user = auth.currentUser; 

  // Prevent logged-in users from accessing login or signup pages
  if ((to.name === 'login' || to.name === 'SignUp') && user) {
    next({ name: 'Menu' }); // Redirect to Menu or other authorized route
    return;
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !user) {
    next({ name: 'login' }); // Redirect to login page
    return;
  }

  // Allow navigation for all other cases
  next();
});

export default router;