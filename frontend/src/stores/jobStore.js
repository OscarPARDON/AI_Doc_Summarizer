import { defineStore } from 'pinia';
import {getJobUpdate} from "@/services/jobPollingService.js";
let intervalId;


export const useJobStore = defineStore('jobs', {
  state: () => ({
    displaySidebar: false,
    pendingJobsList: JSON.parse(localStorage.getItem("savedPendingJobs") || '[]'),
    finishedJobsList: JSON.parse(localStorage.getItem("savedFinishedJobs") || '[]'),
    loading: false,
  }),

  actions: {
    async getFinishedJobs() {
      this.finishedJobsList = JSON.parse(localStorage.getItem("savedFinishedJobs") || '[]');
    },

      async getPendingJobs() {
      this.pendingJobsList = JSON.parse(localStorage.getItem("savedPendingJobs") || '[]');
    },

    async toggleSidebar() {
      if (this.displaySidebar) {
        this.displaySidebar = false;
      } else {
        this.loading = true;
        await this.getFinishedJobs();
        await this.getPendingJobs();
        this.displaySidebar = true;
        this.loading = false;
      }
    },

    async saveFinishedJob(jobUuid, result) {
      await this.getFinishedJobs();
      const exists = this.finishedJobsList.find(v => v.jobUuid === jobUuid);
      if (!exists) {
        this.finishedJobsList.push({ jobUuid, result});
        localStorage.setItem("savedFinishedJobs", JSON.stringify(this.finishedJobsList));
      }
    },

      async savePendingJob(jobUuid, status, filename) {
      await this.getPendingJobs();
      const exists = this.pendingJobsList.find(v => v.jobUuid === jobUuid);
      if (!exists) {
        this.pendingJobsList.push({ jobUuid, status, filename});
        localStorage.setItem("savedPendingJobs", JSON.stringify(this.pendingJobsList));
      }
    },

    async removeFinishedJob(jobUuid) {
      await this.getFinishedJobs();
      this.finishedJobsList = this.finishedJobsList.filter(job => job.jobUuid !== jobUuid);
      localStorage.setItem("savedFinishedJobs", JSON.stringify(this.finishedJobsList))
    },

      async removePendingJob(jobUuid) {
          this.pendingJobsList = this.pendingJobsList.filter(job => job.jobUuid !== jobUuid);
          localStorage.setItem("savedPendingJobs", JSON.stringify(this.pendingJobsList))
        },

    getFinishedJobResult(jobUuid){
      const job = this.finishedJobsList.find(v => v.jobUuid === jobUuid);
      return job ? job.result : null;
    },

      async pendingJobsRefresh() {
        this.loading = true;
        for (const { jobUuid } of this.pendingJobsList) {
                const updatedJob = await getJobUpdate(jobUuid);
                if(updatedJob.result) {
                    this.saveFinishedJob(jobUuid,updatedJob.result)
                    this.removePendingJob(jobUuid)
                }
                else{
                    this.removePendingJob(jobUuid)
                    var filename = this.pendingJobsList.find(v => v.jobUuid === jobUuid).filename;
                    this.savePendingJob(jobUuid,updatedJob.status,filename)
                }
        }
        this.loading = false;
    },

    startPendingJobsPolling(intervalMs = 10 * 1000) {
      if (intervalId) clearInterval(intervalId);
      this.pendingJobsRefresh();
      intervalId = setInterval(() => {
        this.pendingJobsRefresh();
      }, intervalMs);
    },

    stopPendingJobsPolling() {
      if (intervalId) clearInterval(intervalId);
    }
  }
});