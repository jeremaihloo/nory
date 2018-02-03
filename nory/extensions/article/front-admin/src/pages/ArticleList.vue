<template>
  <v-card>
    <v-card-title>
      Articles
      <v-spacer></v-spacer>
      <v-text-field
        append-icon="search"
        label="Search"
        single-line
        hide-details
        v-model="search"
      ></v-text-field>
    </v-card-title>
    <v-data-table
        v-bind:headers="headers"
        v-bind:items="list.items"
        v-bind:search="search"
      >
      <template slot="items" slot-scope="props">
        <td class="text-xs-left" :class="{unpublish:!props.item.published, disabled:!props.item.enabled}">
          <v-btn flat color="primary" @click="goto('/update/' + props.item.id)">{{ props.item.title }}</v-btn>
        </td>
        <td class="text-xs-right">{{ props.item.created_at }}</td>
        <td class="text-xs-right">
          <v-btn color="primary" fab small dark @click="goto('/update/' + props.item.id)">
            <v-icon>edit</v-icon>
          </v-btn>
          <v-btn color="red" fab small dark @click="onRedBtnClicked(props.item)">
            <v-icon>delete</v-icon>
          </v-btn>
        </td>
      </template>
    </v-data-table>
    <div class="text-xs-center pt-2">
      <v-pagination v-model="list.page_index" :length="list.page_total"></v-pagination>
    </div>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      max25chars: v => v.length <= 25 || 'Input too long!',
      tmp: '',
      search: '',
      headers: [
        {
          text: 'Title',
          align: 'left',
          value: 'title'
        },
        { text: 'Created At', value: 'created_at' },
        {
          text: 'Operation',
          align: 'center',
          sortable: false,
          value: 'title'
        }
      ]
    }
  },
  computed: {
    list() {
      return this.$store.state.article.list
    }
  },
  methods: {
    onRedBtnClicked(item) {
      if (item.published) {
        console.log('[article] going to unpublish')
        this.$store
          .dispatch('UN_PUBLISH', item.id)
          .then(res => {
            this.$store.dispatch('GET_ARTICLES')
          })
          .catch(res => {
            console.log(res)
          })
      } else if (item.enabled) {
        console.log('[article] going to disable')
        this.$store
          .dispatch('DISABLE', item.id)
          .then(res => {
            this.$store.dispatch('GET_ARTICLES')
          })
          .catch(res => {
            console.log(res)
          })
      }
    },
    goto(url) {
      this.$router.replace(url)
    }
  },
  created() {
    this.$store.dispatch('GET_ARTICLES')
  }
}
</script>

<style scoped>
.unpublish {
  background-color: cornsilk;
}
.disabled {
  background-color: darkgray;
}
</style>
