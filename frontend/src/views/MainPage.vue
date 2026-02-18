<script setup>
import FileUploadComponent from '@/components/FileUploadComponent.vue'
import SideBarComponent from "@/components/SideBarComponent.vue";
</script>

<template>
  <div class="app-layout">
    <SideBarComponent />
    
    <main class="main-content">
      <div class="header-section">
        <h1 class="app-title">Résumeur de Documents</h1>
        <p class="app-subtitle">Obtenez un résumé clair et précis de vos documents en quelques secondes.</p>
      </div>
      
      <div class="upload-section">
        <FileUploadComponent />
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
  align-items: center;
  justify-content: center;
  padding: 2rem;
  transition: all 0.3s ease;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
  max-width: 600px;
}

.app-title {
  font-size: 3rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 1rem;
  letter-spacing: -0.04em;
  background: linear-gradient(135deg, #1a1a1a 0%, #4b5563 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.app-subtitle {
  font-size: 1.125rem;
  color: #666;
  line-height: 1.6;
}

.upload-section {
  width: 100%;
  max-width: 800px;
}

@media (max-width: 768px) {
  .app-title {
    font-size: 2.25rem;
  }
  
  .header-section {
    margin-bottom: 2rem;
  }
}
</style>
