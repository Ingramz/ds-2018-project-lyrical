<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-3">
        <h4>Chart size</h4>

        <vue-slider
          ref="slider"
          v-model="chartSize"
          v-bind="chartSizeOptions"
          :disabled="locked"
          @drag-end="updateTable"
        />

        <h4>Similarity range</h4>

        <vue-slider
          ref="slider"
          v-model="similarity"
          v-bind="similarityOptions"
          :disabled="locked"
          @drag-end="updateTable"
        />

        <label>
          <input
            v-model="showSimilarities"
            type="checkbox"
          > Show most similar song
        </label>

        <h4>N-gram matches</h4>

        <vue-slider
          ref="slider"
          v-model="ngramMatches"
          v-bind="ngramMatchesOptions"
          :disabled="locked"
          @drag-end="updateTable"
        />

        <h4>Ranking</h4>
        <ul class="list-unstyled">
          <li>
            <label>
              <input
                :disabled="locked"
                v-model="ranking"
                type="radio"
                name="ranking"
                value="1"
                @change="updateTable"
              > Similarity %
            </label>
          </li>
          <li>
            <label>
              <input
                :disabled="locked"
                v-model="ranking"
                type="radio"
                name="ranking"
                value="2"
                @change="updateTable"
              > N-grams matched
            </label>
          </li>
          <li>
            <label>
              <input
                :disabled="locked"
                v-model="ranking"
                type="radio"
                name="ranking"
                value="3"
                @change="updateTable"
              > Average n-gram ranking
            </label>
          </li>
        </ul>
      </div>

      <div class="col">
        <table class="table table-striped table-sm table-hover">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Title</th>
              <th scope="col">Artist</th>
              <th
                v-if="ranking == 1"
                scope="col"
              >Similarity %</th>
              <th
                v-if="ranking == 2"
                scope="col"
              >N-grams matched</th>
              <th
                v-if="ranking == 3"
                scope="col"
              >Average n-gram ranking</th>
              <th
                v-if="ranking == 4"
                scope="col"
              >Weighted average n-gram ranking</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(song, index) in chart"
              :key="index"
              @click="$router.push({ path: 'song/' + song.id })"
            >
              <th scope="row">{{ index + 1 }}</th>
              <td>
                {{ song.title }}
                <template v-if="showSimilarities">
                  <br>
                  <small>Similar to <em>{{ song.top_song.title }}</em> by {{ song.top_song.artist }}</small>
                </template>
              </td>
              <td>{{ song.artist }}</td>
              <td v-if="ranking == 1">{{ formatDecimal(song.topSimilarityPercentage * 100) }}</td>
              <td v-if="ranking == 2">{{ song.ngrams_matched }}</td>
              <td v-if="ranking == 3">{{ formatDecimal(song.averageRanking) }}</td>
              <td v-if="ranking == 4">{{ formatDecimal(song.weightedAverageRanking) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showSimilarities: false,
      chart: [],
      locked: false,
      ranking: 2,
      similarity: [5, 50],
      similarityOptions: {
        min: 0,
        max: 100,
        tooltip: 'hover',
        formatter: '{value}%'
      },
      ngramMatches: [1000, 9000],
      ngramMatchesOptions: {
        min: 0,
        max: 10000,
        tooltip: 'hover'
      },
      chartSize: 100,
      chartSizeOptions: {
        min: 10,
        max: 200,
        tooltip: 'hover'
      }
    }
  },
  created() {
    this.updateTable()
  },
  methods: {
    alert() {
      window.alert('lol')
    },
    log(msg) {
      console.log(msg)
    },
    formatDecimal(value) {
      let val = (value / 1).toFixed(2).replace(',', '.')
      return val
    },
    async updateTable() {
      this.locked = true
      const chart = await this.$axios.$get('/ws/search', {
        params: {
          rankingType: this.ranking,
          similarityMin: this.similarity[0],
          similarityMax: this.similarity[1],
          ngramsMin: this.ngramMatches[0],
          ngramsMax: this.ngramMatches[1],
          size: this.chartSize
        }
      })
      this.chart = chart
      this.locked = false
    }
  }
}
</script>

<style>
h4 {
  margin-top: 3px;
}
</style>
