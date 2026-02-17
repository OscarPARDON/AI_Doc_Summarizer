// import axios from "axios"
//
// const CHUNK_SIZE = 1024 * 1024 * 2 // 2MB
//
// export default async function chunkAndSend(file){
//   const totalChunks = Math.ceil(file.size / CHUNK_SIZE)
//   const fileId = crypto.randomUUID()
//
//   for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
//     const start = chunkIndex * CHUNK_SIZE
//     const end = Math.min(start + CHUNK_SIZE, file.size)
//     const chunk = file.slice(start, end)
//
//     const formData = new FormData()
//     formData.append("UploadFile", chunk)
//     formData.append("fileId", fileId)
//     formData.append("chunkIndex", chunkIndex)
//     formData.append("totalChunks", totalChunks)
//     formData.append("fileName", file.name)
//
//     await axios.post("http://localhost:8000/file/upload-chunk", formData)
//
//     console.log(`Chunk ${chunkIndex + 1}/${totalChunks} envoyé`)
//   }
//
//   console.log("Upload terminé !")
// }

import * as tus from 'tus-js-client'

export default function uploadFIle(file){
  var upload = new tus.Upload(file, {
    endpoint: 'http://localhost:8000/files/',
    retryDelays: [0, 3000, 5000, 10000, 20000],
    metadata: {
      filename: file.name,
      filetype: file.type,
    },
    onError: function (error) {
      console.log('Upload Failure: ' + error)
    },
    onProgress: function (bytesUploaded, bytesTotal) {
      var percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2)
      console.log(bytesUploaded, bytesTotal, percentage + '%')
    },
    onSuccess: function () {
      console.log('Download %s from %s', upload.file.name, upload.url)
    },
  })
  upload.start()
}
