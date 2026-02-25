<script setup>
import { ref, onMounted, watch } from "vue";
import { useJobStore } from "@/stores/jobStore.js";
import { useRoute, useRouter } from 'vue-router';
import SideBarComponent from "@/components/SideBarComponent.vue";

const route = useRoute();
const router = useRouter();
const jobStore = useJobStore();
const isLoading = ref(true);
const job = ref(null);

const fetchResults = () => {
  isLoading.value = true;
  const data = jobStore.getJob(route.params.jobUuid);
  if (data) {
    job.value = data;
    isLoading.value = false;
  } else {
    // If not found, redirect to home or show error
    router.push('/');
  }
};

onMounted(fetchResults);

// Watch for route changes to update the view when clicking another job in sidebar
watch(() => route.params.jobUuid, fetchResults);

// Watch for changes in the store to update the current job (e.g. after polling update)
watch(() => jobStore.jobsList, () => {
  const data = jobStore.getJob(route.params.jobUuid);
  if (data) {
    job.value = data;
  }
}, { deep: true });

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

      <div v-else-if="job" class="summary-container">
        <!-- Filename display for all statuses -->
        <div class="job-filename">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
            <polyline points="13 2 13 9 20 9"></polyline>
          </svg>
          {{ job.filename }}
        </div>

        <!-- Status 1: Processing -->
        <div v-if="job.statusCode === 1" class="status-card processing">
          <div class="status-icon">
            <div class="loader-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
          <h2>Veuillez patienter, le fichier est en cours de traitement</h2>
          <p class="status-message">{{ job.message }}</p>
        </div>

        <!-- Status 3: Failure -->
        <div v-else-if="job.statusCode === 3" class="status-card failure">
          <div class="status-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
          </div>
          <h2>Echec du traitement de votre fichier</h2>
          <p class="status-message">{{ job.message }}</p>
        </div>

        <!-- Status 2: Success -->
        <div v-else-if="job.statusCode === 2 && job.result" class="summary-card">
          <div class="card-header">
            <span class="doc-type">{{ job.result.type_document }}</span>
            <span class="doc-lang">{{ job.result.langue }}</span>
          </div>

          <h1 class="summary-title">{{ job.result.titre }}</h1>

          <div class="summary-body">
            <p class="summary-text">{{ job.result.resume }}</p>
          </div>

          <div class="keywords-section" v-if="job.result.mots_cles && job.result.mots_cles.length">
            <h3>Mots-clés</h3>
            <div class="keywords-list">
              <span v-for="keyword in job.result.mots_cles" :key="keyword" class="keyword-badge">
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

.job-filename {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ca3af;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1rem;
  padding-left: 0.5rem;
}

.summary-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.status-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 24px;
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.status-card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.status-message {
  color: #6b7280;
  font-size: 1.1rem;
  max-width: 500px;
  line-height: 1.5;
}

.status-icon {
  margin-bottom: 0.5rem;
}

/* Loader dots animation from Sidebar */
.loader-dots {
  display: flex;
  gap: 8px;
}

.loader-dots span {
  width: 12px;
  height: 12px;
  background: #3b82f6;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loader-dots span:nth-child(1) { animation-delay: -0.32s; }
.loader-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
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
