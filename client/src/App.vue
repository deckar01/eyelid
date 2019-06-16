<template>
  <div id="app" class="container desktop">
    <section class="section">
      <div class="level">
        <div class="level-item">
          <img id="logo" src="./assets/eyelid.png" alt="eyelid" :class="{small: auth.access_token}"/>
        </div>
        <div class="ghost-level level-right">
          <a v-show="auth.access_token" class="button is-danger is-outlined" @click="logout">logout</a>
        </div>
      </div>
      <div v-show="!auth.access_token">
        <LoginForm @auth="setAuth"/>
      </div>
      <div v-show="auth.access_token">
        <div v-if="!create">
          <a class="button title is-fullwidth is-primary" @click="addFeed">
            + new time lapse
          </a>
          
          <FeedList :token="auth.access_token" @expired="reauth"/>
        </div>
        <div v-else>
          <FeedCreator :token="auth.access_token" @close="create = false" @expired="reauth"/>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import FeedCreator from './components/FeedCreator.vue'
import FeedList from './components/FeedList.vue'
import LoginForm from './components/LoginForm.vue'

axios.defaults.baseURL = 'http://localhost:8081';

export default {
  name: 'app',
  components: {
    FeedList,
    FeedCreator,
    LoginForm,
  },
  data: () => ({
    create: false,
    auth: {},
  }),
  beforeMount() {
    const auth = window.sessionStorage.auth
    if (auth) {
      this.auth = JSON.parse(auth)
    }
  },
  methods: {
    addFeed() {
      this.create = true
    },
    setAuth(auth) {
      window.sessionStorage.auth = JSON.stringify(auth)
      this.auth = auth
    },
    async reauth() {
      try {
        const headers = {Authorization: `Bearer ${this.auth.refresh_token}`}
        const response = await axios.post('/api/v1/security/refresh', null, {headers})
        this.setAuth({
          ...this.auth,
          access_token: response.data.refresh_token,
        })
      } catch(e) {
        this.logout()
      }
    },
    logout() {
      this.setAuth({})
    },
  },
}
</script>

<style lang="scss">
@import "bulma";

html, body {
  background-color: #e1eae5;
  height: 100%;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#logo {
  width: 256px;
  transition: width 350ms ease-in-out;
  
  &.small {
    width: 128px;
  }
}

.level.collapse {
  margin-bottom: -36px;
}

.ghost-level {
  width: 0;
}

.box {
  background-color: rgba(255, 255, 255, 0.5);
  
  .box {
    box-shadow: 0 0 0 1px rgba($black, 0.1);
  }
}
</style>
