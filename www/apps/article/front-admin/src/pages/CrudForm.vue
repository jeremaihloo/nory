<template lang="pug">
v-layout
  v-flex(xs8)
    form(@submit.prevent='onSubmit')
      div(slot="buttons",class="my-4")
        <markdown-editor v-model="article.content" ref="markdownEditor"></markdown-editor>
        v-btn(color="primary", dark, type='button', @click="onSave") {{$t('Save')}}
          v-icon(right, dark) send
        v-btn(color="primary", dark, type='button', @click="onPublish") {{$t('Publish')}}
          v-icon(right, dark) send
</template>

<script>
import markdownEditor from 'vue-simplemde/src/markdown-editor'
export default {
  components: {
    markdownEditor
  },
  computed: {
    article: {
      get: function() {
        return this.$store.state.article
      },
      set: function(value) {
        this.$store.commit('SAVE', value)
      }
    }
  },
  methods: {
    updateFields() {},
    onSave() {
      this.$store.dispatch('SAVE', this.article)
    },
    onPublish(data) {
      this.$store.dispatch('PUBLISH', this.content)
    }
  }
}
</script>

<style>
@import 'simplemde/dist/simplemde.min.css';
</style>