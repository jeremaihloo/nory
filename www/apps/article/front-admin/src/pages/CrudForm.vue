<template lang="pug">
v-layout
  v-flex(xs8)
    form(@submit.prevent='onSubmit')
      div(slot="buttons",class="my-4")
        <markdown-editor v-model="article.content" ref="markdownEditor" preview-class="markdown-body" :highlight="true"></markdown-editor>
        v-btn(color="primary", dark, type='button', @click="onSave") {{$t('Save')}}
          v-icon(right, dark) send
        v-btn(color="primary", dark, type='button', @click="onPublish") {{$t('Publish')}}
          v-icon(right, dark) send
</template>

<script>
import hljs from 'highlight.js'
window.hljs = hljs

import markdownEditor from 'vue-simplemde/src/markdown-editor'
export default {
  components: {
    markdownEditor
  },
  computed: {
    article: {
      get: function() {
        console.log('[article] action', this.$route.params.action)
        if (this.$route.params.action === 'create') {
          return {
            content: this.$store.state.article[this.$route.params.action]
              .content
          }
        }
        return this.$store.state.article[this.$route.params.action]
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
      if (this.article.id) {
        this.$store.dispatch('PUBLISH', this.article.id)
      }
    }
  },
  created() {
    if (this.$route.params.id) {
      console.log('article id', this.$route.params.id)
      this.$store.dispatch('GET_ARTICLE', this.$route.params.id)
    }
  }
}
</script>

<style>
@import 'simplemde/dist/simplemde.min.css';
@import 'github-markdown-css';
@import 'highlight.js/styles/atom-one-dark.css';

code::before,
code::after {
  content: '';
  letter-spacing: -1px;
}
.editor-preview-side pre,
.editor-preview pre {
  color: #abb2bf !important;
  background: #282c34 !important;
}
</style>