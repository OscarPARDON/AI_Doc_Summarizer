import { createRouter, createWebHistory } from 'vue-router';
import MainPage from "@/views/MainPage.vue";
import SummariesPage from "@/views/SummariesPage.vue";

const routes = [
{ path: "/" , component: MainPage},
  {path: "/summary/:jobUuid",component: SummariesPage},

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;