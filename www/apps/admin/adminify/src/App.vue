<template>
  <v-app>
    <v-snackbar
      :timeout="3000"
      :multi-line="mode === 'multi-line'"
      :vertical="mode === 'vertical'"
      v-model="snackbar"
    >
      {{ text }}
      <v-btn dark flat @click.native="snackbar.snackbar = false">Close</v-btn>
    </v-snackbar>
    <transition mode="out-in">
      <router-view></router-view>
    </transition>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data() {
    return {
      snackbar: true,
      color: '',
      mode: '',
      timeout: 6000,
      text: "Hello, I'm a snackbar"
    }
  },
  computed: {
    ...mapState(['message'])
  },
  methods: {},
  created() {
    // this.$http.get('/users').then(({data}) => console.log(data))
  }
}
</script>

