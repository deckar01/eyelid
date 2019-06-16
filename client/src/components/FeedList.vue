<template>
  <div>
    <div class="box">
      <h2 class="title is-2">
        Time Lapses
      </h2>
      
      <hr/>
      
      <p v-if="!feedsLoaded">
        Loading...
      </p>
      <p v-if="noFeeds">
        There are no feeds yet. Add one using the button above.
      </p>
      <div v-if="anyFeeds">
        <FeedPreview v-for="feed in feeds" :feed="feed" :key="feed.name"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import FeedPreview from './FeedPreview.vue'

export default {
  name: 'FeedCreator',
  components: {
    FeedPreview,
  },
  props: {
    token: String,
  },
  data: () => ({
    feeds: null,
    loop: null,
  }),
  computed: {
    feedsLoaded() { return this.feeds !== null },
    anyFeeds() { return this.feedsLoaded && this.feeds.length > 0 },
    noFeeds() { return this.feedsLoaded && this.feeds.length == 0 },
  },
  mounted() {
    this.update();
  },
  beforeDestroy() {
    clearTimeout(this.loop)
  },
  watch: {
    token() {
      clearTimeout(this.loop)
      this.update()
    }
  },
  methods: {
    async update() {
      try {
        if (this.token) {
          const headers = {Authorization: `Bearer ${this.token}`}
          const response = await axios.get('/api/v1/timelapses/', {headers})
          this.feeds = response.data.result
        }
      } catch(e) {
        this.$emit('expired')
      }
      this.loop = setTimeout(() => this.update(), 5000)
    },
    save() {
      console.log({
        name: this.name,
        url: this.url,
        startDate: this.startDate,
      })
    }
  }
}
</script>

<style>
.field > .control.is-fullwidth {
  flex: 1;
}
</style>
