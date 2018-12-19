<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Song extends Model
{
    protected $fillable = [
      'ngrams_matched',
      'artist',
      'title',
      'lyrics',
      'averageRanking',
      'weightedAverageRanking',
      'topSimilarityPercentage',
      'top_song_id'
    ];

    public function topSong() {
        return $this->hasOne('App\TopSong', 'id', 'top_song_id');
    }

    public function ngrams() {
        return $this->belongsToMany('App\Ngram')->withCount('popularSongs')->orderBy('popular_songs_count', 'DESC');
    }

    public function ngramChartSongs() {
       return $this->hasManyThrough('App\TopSong', 'App\Ngram');
    }
}
