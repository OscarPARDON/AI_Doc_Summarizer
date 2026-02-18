<template>
  <div
    class="sidebar"
    :class="{ 'sidebar-open': savedStore.displaySidebar }"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <!-- Toggle Sidebar button -->
    <button @click="savedStore.toggleSidebar()" class="sidebar-toggle">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path v-if="!savedStore.displaySidebar" d="M3 12h18M3 6h18M3 18h18"></path>
        <path v-else d="M18 6L6 18M6 6l12 12"></path>
      </svg>
    </button>

    <!-- Loading Spinner -->
    <div v-if="savedStore.loading" class="loading-container">
      <div class="loading-spinner">
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
      </div>
      <div class="loading-text">
        <div class="loading-title">Chargement des données</div>
      </div>
    </div>

    <!-- Sidebar content -->
    <div v-else class="sidebar-content">
      <div class="sidebar-header">
        <h2 class="sidebar-title">Vos résumés</h2>
        <div class="item-count">{{ savedStore.pendingJobsList.length + savedStore.finishedJobsList.length }} résumé{{ savedStore.pendingJobsList.length + savedStore.finishedJobsList.length !== 1 ? 's' : '' }}</div>
      </div>

      <div class="items-list">
        <div v-if="savedStore.pendingJobsList.length + savedStore.finishedJobsList.length === 0" class="empty-state">
          <div class="empty-icon">📑</div>
          <p>Aucun résumé</p>
          <small>Importez un fichier pour obtenir son résumé</small>
        </div>

        <router-link v-for="job in savedStore.finishedJobsList" :key="job.jobUuid" :to="`/summary/${job.jobUuid}`" custom v-slot="{ navigate, href }">
        <div @click="navigate" class="summary-item">
          <div class="summary-header">
            <div class="summary-title">{{ job.result.titre }}</div>
            <button @click.stop="savedStore.removeFinishedJob(job.jobUuid)" class="remove-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
        </router-link>

        <div v-for="job in savedStore.pendingJobsList" :key="job.jobUuid"  class="summary-item pending">
          <div class="summary-header">
            <div class="summary-title">{{ job.fileTitle }}</div>
            <div class="loader-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile -->
    <div v-if="savedStore.displaySidebar" @click="savedStore.toggleSidebar()" class="sidebar-backdrop"></div>
  </div>
</template>
<script setup>
import {onMounted, onUnmounted, ref} from 'vue';
import {useJobStore} from '../stores/jobStore.js';

const savedStore = useJobStore();

// Variables pour la gestion du swipe
const touchStartX = ref(0);
const touchStartY = ref(0);
const touchEndX = ref(0);
const touchEndY = ref(0);
const minSwipeDistance = 50; // Distance minimale pour considérer un swipe
const maxVerticalDistance = 100; // Distance verticale maximale pour un swipe horizontal

// Gestion du début du touch
const handleTouchStart = (e) => {
  touchStartX.value = e.touches[0].clientX;
  touchStartY.value = e.touches[0].clientY;
};

// Gestion du mouvement du touch
const handleTouchMove = (e) => {
  // Empêcher le scroll par défaut pendant le swipe
  if (savedStore.displaySidebar) {
    e.preventDefault();
  }
};

// Gestion de la fin du touch
const handleTouchEnd = (e) => {
  touchEndX.value = e.changedTouches[0].clientX;
  touchEndY.value = e.changedTouches[0].clientY;

  handleSwipe();
};

const handleSwipe = () => {
  const deltaX = touchStartX.value - touchEndX.value;
  const deltaY = Math.abs(touchStartY.value - touchEndY.value);

  if (
    deltaX > minSwipeDistance &&
    deltaY < maxVerticalDistance &&
    savedStore.displaySidebar
  ) {
    savedStore.toggleSidebar();
  }
};

onMounted(() => {
  savedStore.startPendingJobsPolling();
});

onUnmounted(() => {
  savedStore.stopPendingJobsPolling();
});
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 320px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  transform: translateX(-100%);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.02);
}

.sidebar-open {
  transform: translateX(0);
}

.sidebar-toggle {
  position: absolute;
  top: 1.5rem;
  right: -50px;
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  color: #1a1a1a;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.sidebar-toggle:hover {
  transform: scale(1.05);
  background: #fcfcfc;
}

.sidebar-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 2rem 1.5rem;
}

.sidebar-header {
  margin-bottom: 2.5rem;
}

.sidebar-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.item-count {
  color: #666;
  font-size: 0.85rem;
  font-weight: 500;
}

.items-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  color: #999;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-weight: 600;
  color: #666;
  margin-bottom: 0.25rem;
}

.empty-state small {
  font-size: 0.8rem;
}

.summary-item {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.summary-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  transform: translateY(-1px);
}

.summary-item.pending {
  background: #fafafa;
  border-style: dashed;
  cursor: default;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-title {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 0.5rem;
}

.remove-btn {
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
  padding: 0.2rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.remove-btn:hover {
  color: #ef4444;
  background: #fee2e2;
}

.loader-dots {
  display: flex;
  gap: 3px;
}

.loader-dots span {
  width: 4px;
  height: 4px;
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

.sidebar-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(2px);
  z-index: -1;
}

.items-list::-webkit-scrollbar {
  width: 4px;
}

.items-list::-webkit-scrollbar-track {
  background: transparent;
}

.items-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 280px;
  }
}

.loading-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.spinner-ring {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(59, 130, 246, 0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-title {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}
</style>