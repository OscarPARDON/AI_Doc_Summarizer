<script setup>

import uploadFIle from "@/services/fileUploadService.js";

const handleFileChange = (event) => {
  const file = event.target.files[0]
  uploadFIle(file)
}

</script>

<template>
  <input type="file" @change="handleFileChange" />
</template>