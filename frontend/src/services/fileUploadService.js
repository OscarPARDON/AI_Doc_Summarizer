import axios from "axios"

const CHUNK_SIZE = 1024 * 1024 * 2 // 2MB

async function chunkAndSend(file){
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE)
  const fileId = crypto.randomUUID()

  for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
    const start = chunkIndex * CHUNK_SIZE
    const end = Math.min(start + CHUNK_SIZE, file.size)
    const chunk = file.slice(start, end)

    const formData = new FormData()
    formData.append("file", chunk)
    formData.append("fileId", fileId)
    formData.append("chunkIndex", chunkIndex)
    formData.append("totalChunks", totalChunks)
    formData.append("fileName", file.name)

    await axios.post("http://localhost:8000/file/upload-chunk", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    })

    console.log(`Chunk ${chunkIndex + 1}/${totalChunks} envoyé`)
  }

  console.log("Upload terminé !")
}