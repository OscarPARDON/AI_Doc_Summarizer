<script setup>

import chunkAndSend from '@/services/fileUploadService.js'

const handleFileChange = (event) => {
  const file = event.target.files[0]
  chunkAndSend(file)
}

</script>

<template>
  <input type="file" @change="handleFileChange" />
</template>