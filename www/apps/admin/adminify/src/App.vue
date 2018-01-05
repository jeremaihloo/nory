<template>
  <v-app>
    <v-snackbar
      :timeout="snackbar.timeout"
      :top="snackbar.y === 'top'"
      :bottom="snackbar.y === 'bottom'"
      :right="snackbar.x === 'right'"
      :left="snackbar.x === 'left'"
      :multi-line="snackbar.mode === 'multi-line'"
      :vertical="snackbar.mode === 'vertical'"
      v-model="snackbar.snackbar"
    >
      {{ snackbar.text }}
      <v-btn flat color="primary" @click.native="snackbar.snackbar = false">Close</v-btn>
    </v-snackbar>
    <transition mode="out-in">
      <router-view></router-view>
    </transition>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['message', 'snackbar'])
  },
  methods: {},
  created() {
    // this.$http.get('/users').then(({data}) => console.log(data))
  }
}
</script>

