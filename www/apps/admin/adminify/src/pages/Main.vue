<template lang="pug">
v-app(:dark="dark",standalone)
  v-navigation-drawer(v-model='drawer',:mini-variant.sync="mini", persistent,enable-resize-watcher, :dark="dark")
    .pa-3.text-xs-center(v-show="!mini")
      div.display-2.py-4 Adminify
      p {{$t('An admin dashboard based on Vuetify')}}
      div(style="padding-left:5em")
        v-switch(:label="(!dark ? 'Light' : 'Dark') + ' Theme'", v-model="dark", :dark="dark", hide-details, @change='onDarkChange')
      div
        v-btn(dark, tag="a", href="https://github.com/wxs77577/adminify", primary) 
          v-icon(left, dark) star
          span Github 
    .pa-3.text-xs-center(v-show="mini")
      .display-2 A
    v-divider
    v-list(dense)
      template(v-for='item in menu')
        v-list-group(v-if='item.items', v-bind:group='item.group')
          v-list-tile(:to='item.href', slot='item', :title="item.title")
            v-list-tile-action
              v-icon() {{ item.icon }}
            v-list-tile-content
              v-list-tile-title {{ $t(item.title) }}
            v-list-tile-action
              v-icon() keyboard_arrow_down
          
          v-list-tile(v-for='subItem in item.items', :key='subItem.href', @click="goto(subItem)", ripple, v-bind:disabled='subItem.disabled')
            v-list-tile-action(v-if='subItem.icon')
              v-icon.success--text {{ subItem.icon }}
            v-list-tile-content
              v-list-tile-title {{ $t(subItem.title) }}
        v-subheader(v-else-if='item.header') {{ item.header }}
        v-divider(v-else-if='item.divider')
        v-list-tile(v-else, @click="goto(item)", router, ripple, v-bind:disabled='item.disabled', :title="item.title")
          v-list-tile-action
            v-icon() {{ item.icon }}
          v-list-tile-content
            v-list-tile-title {{ $t(item.title) }}
          v-list-tile-action(v-if='item.subAction')
            v-icon.success--text {{ item.subAction }}
  v-toolbar.darken-1(fixed,dark,:class="theme") 
    v-toolbar-side-icon(dark, @click='drawer = !drawer')
    v-toolbar-title {{$t(pageTitle)}}
    v-spacer
    v-menu(offset-y)
      v-btn(icon, dark, slot="activator")
        v-icon(dark) language
      v-list
        v-list-tile(v-for="lang in locales" :key="lang",@mouseover.native="changeLocale(lang)")
          v-list-tile-title {{lang}}
    v-menu(offset-y)
      v-btn(icon, dark, slot="activator")
        v-icon(dark) format_paint
      v-list
        v-list-tile(v-for="n in colors", :key="n", :class="n",@mouseover.native="theme = n")
  main
    v-container.pa-4(fluid)
        v-alert(v-bind='message', v-model='message.body', dismissible) {{message.body}}
        .admin-content
          v-slide-y-transition(mode='out-in')
            html-panel(:url.asyc='adminContentUrl')
</template>

<script>
import { mapState } from 'vuex'
import HtmlPanel from '../components/HtmlPanel'
import * as TYPES from '../store/mutation_type'

export default {
  components: {
    HtmlPanel
  },
  data() {
    return {
      theme: 'primary',
      mini: false,
      drawer: true,
      locales: ['en-US', 'zh-CN'],
      colors: ['blue', 'green', 'purple', 'red'],
      staticMenu: [
        { divider: true },
        { header: 'System' },
        { href: '/settings', title: 'Settings', icon: 'settings' },
        { href: '/logout', icon: 'lock', title: 'Logout' }
      ]
    }
  },
  computed: {
    ...mapState(['message', 'pageTitle', 'adminContentUrl']),
    menu() {
      const staticMenu = Object.assign([], this.staticMenu)
      const stateMenu = this.$store.state.menu
      return Object.assign(staticMenu, stateMenu)
    },
    dark: {
      get: function() {
        return this.$store.state.dark
      },
      set: function() {
        this.$store.commit(TYPES.DARK_MODE, !this.$store.state.dark)
      }
    }
  },
  methods: {
    changeLocale(to) {
      global.helper.ls.set('locale', to)
      this.$i18n.locale = to
    },
    fetchMenu() {
      // fetch menu from server
      // this.$http.get('menu').then(({data}) => this.$store.commit('setMenu', data))
    },
    goto(item) {
      if (item.target === 'admin-content') {
        this.$store.commit(TYPES.CHANGE_ADMIN_CONTENT_URL, item.href)
      }
    },
    onDarkChange() {}
  },

  created() {
    this.fetchMenu()
  }
}
</script>

<style lang="stylus" scoped>
.admin-content {
  width: 100%;
  height: 100vh;
}
</style>
