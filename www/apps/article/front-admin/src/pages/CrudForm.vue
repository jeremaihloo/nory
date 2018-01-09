<template lang="pug">
v-layout
  v-flex(xs8)
    form(@submit.prevent='onSubmit')
      div(slot="buttons",class="my-4")
        <markdown-editor @input="$store.commit('SAVE', article)" v-model="article.content" ref="markdownEditor" preview-class="markdown-body" :highlight="true"></markdown-editor>
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
  data() {
    return {
      article: {
        content: '你好，中国！'
      }
    }
  },
  methods: {
    updateFields() {},
    onSave() {
      this.$store.dispatch('SAVE', this.article).then(res => {
        if (this.$route.params.action === 'create') {
          this.$router.push(`/update/${res.data.body.id}`)
        }
      })
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
      this.$store
        .dispatch('GET_ARTICLE', this.$route.params.id)
        .then(res => {
          this.article = this.$store.state.article[this.$route.params.action]
        })
        .catch(res => {})
    } else {
      if (this.$route.params.action) {
        this.article = this.$store.state.article[this.$route.params.action]
      }
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