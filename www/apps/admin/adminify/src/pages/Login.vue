<template lang="pug">
div
  v-dialog(:value='true', persistent='')
    v-card(hover='', style='background:white')
        v-card-title.white--text.deep-purple.darken-1
          .text-xs-center  {{$t("Login")}}
        v-card-text.pt-4
          v-form(v-model='model', :error='onError', :fields='fields', :autoSubmit=False, @submit='onSubmit', submitButtonText="Login")
            .flex.pb-2
              small {{$t("* Indicates required field")}}
            
</template>

<style>
body {
  background: #666 !important;
}
</style>

<script>
import * as TYPES from '../store/mutation_type'
export default {
  data() {
    return {
      model: {
        email: '1006397539@qq.com',
        password: '111'
      },

      fields: {
        email: { label: 'Username' },
        password: { label: 'Password', type: 'password' }
      },
      show: true
    }
  },
  methods: {
    onSubmit() {
      this.$store
        .dispatch(TYPES.DO_LOGIN, {
          email: this.model.email,
          password: this.model.password
        })
        .then(res => {
          console.log(res)
          if (res.data.ok) {
            this.$store
              .dispatch(TYPES.DO_GET_MENU)
              .then(r => {
                if (r.data.ok) {
                  this.$router.replace('/')
                } else {
                  console.log(r)
                }
              })
              .catch(r => {
                console.log(r)
              })
          }
        })
        .catch(res => {
          console.log(res)
        })
    },
    onError(e) {
      console.log('login error:', e)
    }
  },

  mounted() {}
}
</script>
