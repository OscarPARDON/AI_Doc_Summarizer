import axios from 'axios';
import {useJobStore} from '@/stores/jobStore.js'

export async function getJobUpdate(jobUuid) {
  try {
    const response = await axios.get('http://localhost:8000/jobs/' + jobUuid);

    // Axios met les données dans response.data
    const jobData = response.data;

    if (response.status === 200) {

      // Parser le JSON contenu dans result
      const parsedResult = JSON.parse(jobData.result);

      return {
        ...jobData,
        result: parsedResult
      };

    }

    else {
      console.error("Erreur dans la réponse :", response.status);
      return null;
    }

  } catch (error) {
    if (error.status === 404){
      const jobStore = useJobStore()
      jobStore.removeJob(jobUuid)
    }
    console.error("Erreur Axios :", error);
    return null;
  }
}
