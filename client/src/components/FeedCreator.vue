<template>
  <div class="box">
    <h2 class="title is-2">
      New Time Lapse
    </h2>
    
    <p class="content has-text-grey">
      Photos will be captured from the webcam stream on a
      regular interval, then rendered into a timelapse video.
    </p>
    
    <div class="box">
      <h4 class="title is-4">
        Stream Details
      </h4>
      
      <hr/>
      
      <div class="field">
        <label class="label">Name</label>
        <div class="control">
          <input class="input" type="text" placeholder="Pick a Name" v-model="name">
        </div>
      </div>
      
      <div class="field">
        <label class="label">URL</label>
        <div class="control">
          <input class="input" type="text" placeholder="Enter the URL of the Webcam Stream" v-model="url">
        </div>
      </div>
    </div>
    
    <div class="box">
      <h4 class="title is-4">
        Recording Options
      </h4>
      
      <hr/>
      
      <div class="field">
        <label class="label">Start Time</label>
        <div class="control">
          <datepicker placeholder="Select a Time" v-model="startTime" :config="timeOnly"/>
        </div>
      </div>
      
      <div class="field">
        <label class="label">End Time</label>
        <div class="control">
          <datepicker placeholder="Select a Time" v-model="endTime" :config="timeOnly"/>
        </div>
      </div>
      
      <div class="field">
        <label class="label">Start Date</label>
        <div class="control">
          <datepicker placeholder="Select a Date" v-model="startDate"/>
        </div>
      </div>
      
      <div class="field">
        <label class="label">Multiple Days?</label>
        <div class="control">
          <label class="radio">
            <input type="radio" :value="false" v-model="multipleDays">
            No
          </label>
          <label class="radio">
            <input type="radio" :value="true" v-model="multipleDays">
            Yes
          </label>
          &nbsp;
          <span v-if="multipleDays" class="content has-text-grey">
            Photos will be captured across multiple days.
          </span>
        </div>
      </div>
      
      <div class="field" v-if="multipleDays">
        <label class="label">End Date</label>
        <div class="control">
          <datepicker placeholder="Select a Date" v-model="endDate"/>
        </div>
      </div>
      
      <div v-if="multipleDays" class="field">
        <label class="label">One frame per day?</label>
        <div class="control">
          <label class="radio">
            <input type="radio" :value="false" v-model="oncePerDay">
            No
          </label>
          <label class="radio">
            <input type="radio" :value="true" v-model="oncePerDay">
            Yes
          </label>
          &nbsp;
          <span v-if="oncePerDay" class="content has-text-grey">
            One frame will be captured per day.
          </span>
        </div>
      </div>
    </div>

    <div class="box">
      <h4 class="title is-4">
        Video Options
      </h4>
      
      <hr/>
      
      <div class="field">
        <label class="label">Frame Rate (fps)</label>
        <div class="control">
          <input class="input" type="number" v-model="frameRate">
        </div>
      </div>
      
      <div class="field">
        <label class="label">Duration (h:m:s)</label>
        <div class="control">
          <input v-if="!lockDuration" class="input" type="text" v-model="duration">
          <input v-else class="input" type="text" :value="toTimestamp(durationByDays)" disabled>
        </div>
      </div>
      
      <div class="field">
        <label class="label">Total Frames</label>
        <div class="control">
          <input class="input" type="text" :value="frames" disabled>
        </div>
      </div>
      
      <div class="field">
        <label class="label">Sample Frequency (h:m:s)</label>
        <div class="control">
          <input class="input" type="text" :value="toTimestamp(frequency)" disabled>
        </div>
      </div>
    </div>
    
    <div class="level">
      <div class="level-item">
        <a class="button is-info is-large is-fullwidth" :disabled="!valid" @click="save">Save</a>
      </div>
    </div>
    
    <div class="level">
      <div class="level-item">
        <a class="button is-danger is-outlined" @click="$emit('close')">Cancel</a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Datepicker from 'deckar01-vue-bulma-datepicker'
import Progress from './Progress.vue'

export default {
  name: 'FeedCreator',
  components: {
    Datepicker,
    Progress,
  },
  props: {
    token: String,
  },
  data: () => ({
    name: '',
    url: '',
    frameRate: 24,
    duration: '1:00',
    multipleDays: false,
    oncePerDay: false,
    startDate: null,
    endDate: null,
    startTime: '6:00 AM',
    endTime: '6:00 PM',
  }),
  watch: {
    multipleDays() {
      this.endDate = null
      this.oncePerDay = false
    }
  },
  computed: {
    lockDuration() { return this.multipleDays && this.oncePerDay },
    millisecondsPerDay() { return 1000*60*60*24 },
    recordingDurationInMS() {
        const startDate = new Date(`${this.startDate} ${this.startTime}`)
        const endDate = new Date(`${this.endDate || this.startDate} ${this.endTime}`)
        return Math.max(0, endDate - startDate)
    },
    recordingDurationInS() { return this.recordingDurationInMS / 1000 },
    frames() { return Math.round((this.lockDuration ? this.durationByDays : this.toSeconds(this.duration)) * this.frameRate) },
    frequency() {
      return (this.recordingDurationInS / this.frames) || null
    },
    durationByDays() {
      const startDate = new Date(`${this.startDate}`)
      const endDate = new Date(`${this.endDate || this.startDate}`)
      const milliseconds = Math.max(0, endDate - startDate)
      return milliseconds / this.millisecondsPerDay / this.frameRate
    },
    timeOnly() {
      return {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:S",
      }
    },
    valid() {
      if (!this.name) {
        console.log('There is no name')
        return false
      }
      if (!this.url) {
        console.log('There is no URL')
        return false
      }
      if (!this.startDate) {
        console.log('There is no date to start')
        return false
      }
      if (!this.multipleDays && this.startTime == this.endTime) {
        console.log('There is no time to record')
        return false
      }
      return true
    }
  },
  methods: {
    toSeconds(duration) {
      const weights = [1, 60, 60, 24]
      const parts = duration.replace(' ', '').split(':').map(t => Number(t || 0)).reverse()
      return parts.reduce((p, c, i) => p + c * weights[i], 0)
    },
    toTimestamp(totalSeconds) {
      const hours = Math.floor(totalSeconds / (60*60))
      const minutes = Math.floor((totalSeconds / 60) % 60)
      const seconds = Math.floor(totalSeconds % 60)
      const ms = Math.round(totalSeconds * 1000) % 1000
      return [hours, minutes, seconds].map(t => `${t}`.padStart(2, '0')).join(':') + (ms ? `.${ms}`.padEnd(4, '0') : '')
    },
    async save() {
      if (!this.valid) return
      try {
        const headers = {Authorization: `Bearer ${this.token}`}
        const feed = {
          name: this.name,
          url: this.url,
          start_date: new Date(`${this.startDate} ${this.startTime}`).toISOString(),
          end_date: new Date(`${this.endDate || this.startDate} ${this.endTime}`).toISOString(),
          frames: this.frames,
          frequency: this.frequency,
          framerate: this.frameRate,
        }
        const response = await axios.post('/api/v1/timelapses/', feed, {headers})
        this.feeds = response.data.result
        this.$emit('close')
      } catch(e) {
        if (e.response.status == 401) this.$emit('expired')
      }
    }
  }
}
</script>

<style>
.field > .control.is-fullwidth {
  flex: 1;
}
</style>
