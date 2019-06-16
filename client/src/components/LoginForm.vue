<template>
  <div class="box">
    <h2 class="title is-2">
      Login
    </h2>
    
    <div class="notification is-danger" v-show="error">
      Login failed.
    </div>
    
    <div class="field">
      <label class="label">Username</label>
      <div class="control">
        <input class="input" type="text" placeholder="Enter your username" v-model="username">
      </div>
    </div>
    
    <div class="field">
      <label class="label">Password</label>
      <div class="control">
        <input class="input" type="password" placeholder="Enter your password" v-model="password" @keyup.enter="login">
      </div>
    </div>
    
    <a class="button is-fullwidth is-large is-primary" :class="{'is-loading': loading}" @click="login">Login</a>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginForm',
  props: {
    token: String,
  },
  data: () => ({
    username: '',
    password: '',
    loading: false,
    error: false,
  }),
  methods: {
    async login() {
      try {
        this.error = false
        this.loading = true
        const response = await axios.post('/api/v1/security/login', {
          "password": this.password,
          "provider": "db",
          "refresh": true,
          "username": this.username
        })
        this.password = ''
        this.$emit('auth', response.data)
      } catch(e) {
        this.error = true
      }
      this.loading = false
    },
  }
}
</script>
