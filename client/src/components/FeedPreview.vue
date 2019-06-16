<template>
  <div class="box">
    <article class="media">
      <div class="media-left">
        <p class="image is-128x128">
          <img :src="feed.preview || 'https://bulma.io/images/placeholders/128x128.png'">
        </p>
      </div>
      <div class="media-content">
        <div class="level">
          <div class="level-left">
            <strong class="title">{{ feed.name }}</strong>
          </div>
          <div v-show="feed.video" class="level-right">
            <a class="button is-info" :href="feed.video">download</a>
          </div>
        </div>
        <div v-if="!captured">
          <ProgressBar :value="feed.progress" :max="feed.frames" loading="is-primary" done="is-info"/>
        </div>
        <div v-else>
          <ProgressBar :value="videoProgress" :max="1" loading="is-info" done="is-info"/>
        </div>
        <div>
          <strong>Status: </strong>
          <span>{{ feed.status }} </span>
          <span v-show="feed.status === 'recording'">({{ percentage }}%)</span>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import ProgressBar from './Progress.vue'

export default {
  name: 'FeedPreview',
  components: {
    ProgressBar,
  },
  props: {
    feed: Object
  },
  computed: {
    percentage() { return Math.round(100 * this.feed.progress / this.feed.frames) },
    captured() { return this.feed.status === 'rendering' || this.feed.status === 'done'},
    videoProgress() { return this.feed.video ? 1 : -1 },
  }
}
</script>
