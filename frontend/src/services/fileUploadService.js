import * as tus from 'tus-js-client'
import {useJobStore} from "@/stores/jobStore.js";

export default function uploadFile(file, options = {}) {
  const { onSuccess, onError, onProgress } = options;
  
  var upload = new tus.Upload(file, {
    endpoint: 'http://localhost:8000/files/',
    retryDelays: [0, 3000, 5000, 10000, 20000],
    metadata: {
      filename: file.name,
      filetype: file.type,
    },
    onError: function (error) {
      console.log('Upload Failure: ' + error);
      if (onError) onError(error);
    },
    onProgress: function (bytesUploaded, bytesTotal) {
      var percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2);
      console.log(bytesUploaded, bytesTotal, percentage + '%');
      if (onProgress) onProgress(percentage);
    },
    onSuccess: function () {
      const jobStore = useJobStore();
      const urlStr = upload.url;
      const uuid = new URL(urlStr).pathname.split('/').filter(Boolean).pop();
      
      jobStore.savePendingJob(uuid, "En cours de traitement : Document importé avec succès", upload.file.name);
      console.log('Download %s from %s', upload.file.name, upload.url);
      
      if (onSuccess) onSuccess(uuid);
    },
  });
  
  upload.start();
}
