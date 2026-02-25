import { defineStore } from 'pinia';
import {getJobUpdate} from "@/services/jobPollingService.js";
let intervalId;


export const useJobStore = defineStore('jobs', {
  state: () => ({
    displaySidebar: false,
    jobsList: JSON.parse(localStorage.getItem("savedJobs") || '[]'),
    loading: false,
  }),

  actions: {

      async getJobs() {
      this.jobsList = JSON.parse(localStorage.getItem("savedJobs") || '[]');
    },

    async toggleSidebar() {
      if (this.displaySidebar) {
        this.displaySidebar = false;
      } else {
        this.loading = true;
        await this.getJobs();
        this.displaySidebar = true;
        this.loading = false;
      }
    },

    async saveJob(jobUuid, filename, statusCode, message, result) {
      await this.getJobs();
      const exists = this.jobsList.find(v => v.jobUuid === jobUuid);
      if (!exists) {
        this.jobsList.push({ jobUuid, filename, statusCode, message, result});
        localStorage.setItem("savedJobs", JSON.stringify(this.jobsList));
      }
    },

    async removeJob(jobUuid) {
      await this.getJobs();
      this.jobsList = this.jobsList.filter(job => job.jobUuid !== jobUuid);
      localStorage.setItem("savedJobs", JSON.stringify(this.jobsList))
    },

    getJob(jobUuid){
      return this.jobsList.find(v => v.jobUuid === jobUuid);
    },

      async jobsRefresh() {
        this.loading = true;
        for (const { jobUuid, statusCode } of this.jobsList) {
            if(statusCode === 1){
               const updatedJob = await getJobUpdate(jobUuid);
               this.removeJob(jobUuid)
               this.saveJob(jobUuid,updatedJob.filename, updatedJob.status_code, updatedJob.message, updatedJob.result)

            }
        }
        this.loading = false;
    },

    startJobsPolling(intervalMs = 10 * 1000) {
      if (intervalId) clearInterval(intervalId);
      this.jobsRefresh();
      intervalId = setInterval(() => {
        this.jobsRefresh();
      }, intervalMs);
    },

    stopJobsPolling() {
      if (intervalId) clearInterval(intervalId);
    }
  }
});