import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from "@/views/WelcomePage.vue";

const routes = [
{ path: "/" , component: WelcomePage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;