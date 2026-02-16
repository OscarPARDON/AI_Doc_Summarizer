<script setup>
import FileUploadComponent from '@/components/FileUploadComponent.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

  </header>

  <main>
    <FileUploadComponent></FileUploadComponent>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

main{
  height: 100vh;
}

</style>