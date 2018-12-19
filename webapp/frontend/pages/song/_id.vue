<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <nuxt-link to="/">Back to search</nuxt-link>

        <h3>{{ song.title }}</h3> by {{ song.artist }}
        <small><a target="_blank" :href="`https://www.youtube.com/results?search_query=` + encodeURIComponent(song.title + ' - ' + song.artist)">Search on YouTube</a></small>

        <p>
          <span
            v-for="(word, index) in lyrics"
            :key="index"
            :class="'word word-' + index"
            :style="{backgroundColor: colormap(Math.sqrt(Math.sqrt(Math.sqrt(word.heat))))}"
            :title="formatDecimal(word.heat * 100) + '%'"
          >{{ word.name }}</span>
        </p>

        <h4>N-gram occurrences</h4>

        <details>
          <ul>
            <li
              v-for="(ngram, index) in Object.keys(song.ngrams || {})"
              :key="index"
            >{{ ngram }} ({{ song.ngrams[ngram] }})</li>
          </ul>
        </details>

        <h4>Top chart songs that share n-grams with this song</h4>
        <details>
          <ul>
            <li
              v-for="(song, index) in song.popularSongs"
              :key="index"
            >{{ song.title }} - {{ song.artist }}</li>
          </ul>
        </details>
      </div>
    </div>
  </div>
</template>

<script>
const interpolate = require('color-interpolate')

export default {
  data() {
    return {
      song: {},
      colormap: interpolate(['white', 'yellow', 'red'])
    }
  },
  computed: {
    lyrics() {
      if (!this.song || !this.song.lyrics) {
        return []
      }

      let ngramIndex = []
      let maxHeat = 1
      Object.keys(this.song.ngrams).forEach(x => {
        ngramIndex[x] = this.song.ngrams[x]
        maxHeat = Math.max(maxHeat, this.song.ngrams[x])
      })

      let heatmap = []
      let words = this.song.lyrics.split(' ')
      for (var i = 0; i < words.length; i++) {
        // prettier-ignore
        let heat =
          Math.max(
            (ngramIndex[words[i - 2] + ' ' + words[i - 1] + ' ' + words[i]] || 0) / maxHeat,
            (ngramIndex[words[i - 1] + ' ' + words[i] + ' ' + words[i + 1]] || 0) / maxHeat,
            (ngramIndex[words[i] + ' ' + words[i + 1] + ' ' + words[i + 2]] || 0) / maxHeat
          )

        heatmap.push({
          name: words[i],
          heat: heat
        })
      }

      return heatmap
    }
  },
  validate({ params }) {
    // Must be a number
    return /^\d+$/.test(params.id)
  },
  created() {
    this.getSong()
  },
  methods: {
    async getSong() {
      let song = await this.$axios.$get(
        '/ws/song/' + this.$route.params.id
      )
      this.song = song
    },
    formatDecimal(value) {
      let val = (value / 1).toFixed(2).replace(',', '.')
      return val
    }
  }
}
</script>

<style>
.word {
  word-wrap: break-word;
}

.word:after {
  content: ' ';
}
</style>
