<template>
  <progress
    v-if="value >= 0"
    class="progress is-large"
    :class="complete ? done : loading"
    :value="value"
    :max="max"
  ></progress>
  <progress
    v-else
    class="progress is-large"
    :class="complete ? done : loading"
    :max="max"
  ></progress>
</template>

<script>
export default {
  name: 'Progress',
  props: {
    value: Number,
    max: Number,
    loading: String,
    done: String,
  },
  computed: {
    complete() { return this.value === this.max },
  },
}
</script>