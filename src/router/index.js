import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import Menu from '../views/Menu.vue'
import Customize from '../views/Customize.vue'
import LogIn from '../views/LogIn.vue';
import SignUp from '../views/SignUp.vue';
import WaitingPage from '../views/WaitingPage.vue';
import UserProfile from '../views/UserProfile.vue';
import Recommend from '../views/Recommend.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView
    // },
    {
      path: '/:catchAll(.*)',
      redirect: '/login',
    },
    {
      path: '/menu',
      name: 'Menu',
      component: Menu
    },
    {
      path: '/customize/:id',
      name: 'Customize',
      component: Customize,
      meta: { requiresAuth: true }
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
      meta: { requiresAuth: true }

    },
    {
      path: '/UserProfile',
      name: 'UserProfile',
      component: UserProfile,
      meta: { requiresAuth: true }

    },
    {
      path: '/Recommend',
      name: 'Recommend',
      component: Recommend,
      meta: { requiresAuth: true }
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

export default router
