<script setup>
import { ref } from 'vue';
import uploadFile from "@/services/fileUploadService.js";
import { useJobStore } from '@/stores/jobStore.js'
const isDragging = ref(false);
const fileInput = ref(null);
const notification = ref(null); // { type: 'success' | 'error', message: string }

const showNotification = (type, message) => {
  notification.value = { type, message };
  // Masquer après 5 secondes
  setTimeout(() => {
    notification.value = null;
  }, 5000);
};

const handleUpload = (file) => {
  if (!file) return;

  uploadFile(file, {
    onSuccess: (uuid) => {

      showNotification('success', `Fichier "${file.name}" importé avec succès !`);
    },
    onError: (error) => {
      showNotification('error', `Erreur lors de l'import : ${error.message || 'Problème de connexion'}`);
    }
  });
};

const handleFileChange = (event) => {
  const jobStore = useJobStore()
  const file = event.target.files[0];
  handleUpload(file);
  jobStore.toggleSidebar()

};

const onDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  handleUpload(file);
};

const onDragOver = () => {
  isDragging.value = true;
};

const onDragLeave = () => {
  isDragging.value = false;
};

const triggerFileInput = () => {
  fileInput.value.click();
};
</script>

<template>
  <div class="upload-container">
    <div 
      class="drop-zone" 
      :class="{ 'is-dragging': isDragging }"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="triggerFileInput"
    >
      <input 
        type="file" 
        ref="fileInput" 
        class="file-input" 
        @change="handleFileChange" 
        accept=".pdf,.doc,.docx,.txt"
      />
      
      <div class="upload-content">
        <div class="upload-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
        </div>
        <h3>Glissez votre document ici</h3>
        <p>ou cliquez pour parcourir vos fichiers</p>
        <div class="file-types">PDF, DOCX, TXT</div>
      </div>
    </div>

    <!-- Notification Toast -->
    <Transition name="toast">
      <div v-if="notification" class="notification" :class="notification.type">
        <div class="notif-icon">
          <svg v-if="notification.type === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <div class="notif-message">{{ notification.message }}</div>
        <button class="notif-close" @click="notification = null">&times;</button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.upload-container {
  width: 100%;
  max-width: 600px;
  margin: 2rem auto;
  position: relative;
}

.drop-zone {
  position: relative;
  width: 100%;
  height: 300px;
  border: 2px dashed rgba(0, 0, 0, 0.1);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  overflow: hidden;
}

.drop-zone:hover {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.02);
  transform: translateY(-2px);
}

.drop-zone.is-dragging {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
  transform: scale(1.02);
}

.file-input {
  display: none;
}

.upload-content {
  text-align: center;
  pointer-events: none;
}

.upload-icon {
  margin-bottom: 1.5rem;
  color: #3b82f6;
  transition: transform 0.3s ease;
}

.drop-zone:hover .upload-icon {
  transform: translateY(-5px);
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

p {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.file-types {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: #f3f4f6;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #4b5563;
  letter-spacing: 0.05em;
}

/* Notifications styles */
.notification {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 2000;
  max-width: 400px;
  animation: slideIn 0.3s ease-out;
}

.notification.success {
  background: #ecfdf5;
  border: 1px solid #10b981;
  color: #065f46;
}

.notification.error {
  background: #fef2f2;
  border: 1px solid #ef4444;
  color: #991b1b;
}

.notif-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notif-message {
  font-size: 0.875rem;
  font-weight: 600;
  flex: 1;
}

.notif-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: inherit;
  opacity: 0.5;
  padding: 0;
  line-height: 1;
}

.notif-close:hover {
  opacity: 1;
}

/* Transitions */
.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  transform: translateY(20px);
  opacity: 0;
}
.toast-leave-to {
  transform: translateX(50px);
  opacity: 0;
}

@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
