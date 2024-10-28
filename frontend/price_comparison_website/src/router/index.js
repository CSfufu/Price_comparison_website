import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RegisterView from '../views/RegisterView.vue';
import LoginView from '../views/LoginView.vue';
import AboutView from "../views/AboutView.vue";
import Services from "../views/Services.vue";
import ProFile from "../views/ProFile.vue";
import SearchView from "../views/SearchView.vue";
import ProductDetail from "../views/ProductDetail.vue";
import HistoryView from "../views/HistoryView.vue";
import PriceHistory from "@/views/PriceHistory.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  // 其他路由
  {
    path: '/about',
    name: 'about',
    component: AboutView,
  },
  {
    path: '/services',
    name: 'services',
    component: Services
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProFile
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  {
    path: '/history',
    name: History,
    component: HistoryView
  },
  {
    path: '/price_history',
    name: PriceHistory,
    component: PriceHistory
  },
  {
    path: '/products/:id/',
    name: 'ProductDetail',
    component: ProductDetail,
    props: true,
  },

];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
