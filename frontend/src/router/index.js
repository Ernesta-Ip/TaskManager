import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import BoardDetailView from '@/views/BoardDetail.vue';
import LoginRedirect from '@/views/LoginRedirect.vue';

const routes = [
  { path: '/', name: 'Root', component: () => import('@/views/Dashboard.vue') },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/board/:id',
    name: 'BoardDetail',
    component: BoardDetailView,
  }, 
  {
    path: '/login_redirect_view', 
    name: 'LoginRedirect',
    component: LoginRedirect,
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   const isAuthenticated = document.cookie.includes('sessionid');
//   const isSkipped = localStorage.getItem('skipAuth') === 'true';

//   if (!isAuthenticated && !isSkipped && to.name !== 'Login') {
//     next({ name: 'Login' });
//   } else {
//     next();
//   }
// }
// );

export default router;