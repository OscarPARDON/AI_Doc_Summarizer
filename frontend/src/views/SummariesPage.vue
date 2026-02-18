<script setup>
import { ref, onMounted, watch } from "vue";
import { useJobStore } from "@/stores/jobStore.js";
import { useRoute, useRouter } from 'vue-router';
import SideBarComponent from "@/components/SideBarComponent.vue";

const route = useRoute();
const router = useRouter();
const jobStore = useJobStore();
const isLoading = ref(true);
const results = ref(null);

const fetchResults = () => {
  isLoading.value = true;
  const data = jobStore.getFinishedJobResult(route.params.jobUuid);
  if (data) {
    results.value = data;
    console.log(results)
    isLoading.value = false;
  } else {
    // If not found, redirect to home or show error
    router.push('/');
  }
};

onMounted(fetchResults);

// Watch for route changes to update the view when clicking another job in sidebar
watch(() => route.params.jobUuid, fetchResults);

const goHome = () => {
  router.push('/');
};
</script>

<template>
  <div class="app-layout">
    <SideBarComponent />

    <main class="main-content">
      <header class="summary-header">
        <button @click="goHome" class="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Retour à l'accueil
        </button>
      </header>

      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Chargement du résumé...</p>
      </div>

      <div v-else-if="results" class="summary-container">
        <div class="summary-card">
          <div class="card-header">
            <span class="doc-type">{{ results.type_document }}</span>
            <span class="doc-lang">{{ results.langue }}</span>
          </div>

          <h1 class="summary-title">{{ results.titre }}</h1>

          <div class="summary-body">
            <p class="summary-text">{{ results.resume }}</p>
          </div>

          <div class="keywords-section" v-if="results.mots_cles && results.mots_cles.length">
            <h3>Mots-clés</h3>
            <div class="keywords-list">
              <span v-for="keyword in results.mots_cles" :key="keyword" class="keyword-badge">
                {{ keyword }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: #fcfcfc;
  width: 100%;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.summary-header {
  margin-bottom: 2rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #666;
  font-weight: 600;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.back-button:hover {
  color: #1a1a1a;
  background: rgba(0, 0, 0, 0.05);
}

.summary-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.summary-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.card-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.doc-type, .doc-lang {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
}

.doc-type {
  background: #eff6ff;
  color: #3b82f6;
}

.doc-lang {
  background: #f3f4f6;
  color: #4b5563;
}

.summary-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 2rem;
  line-height: 1.2;
}

.summary-body {
  margin-bottom: 3rem;
}

.summary-text {
  font-size: 1.125rem;
  line-height: 1.8;
  color: #374151;
  white-space: pre-wrap;
}

.keywords-section h3 {
  font-size: 0.9rem;
  font-weight: 700;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
}

.keywords-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-badge {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  color: #4b5563;
  padding: 0.5rem 1rem;
  border-radius: 100px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.keyword-badge:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(59, 130, 246, 0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .summary-card {
    padding: 1.5rem;
  }
  
  .summary-title {
    font-size: 1.75rem;
  }
}
</style>
