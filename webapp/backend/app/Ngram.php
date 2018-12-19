<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Ngram extends Model
{
    protected $fillable = ['name'];

    protected $with = ['popularSongs'];

    public function popularSongs() {
        return $this->belongsToMany('App\TopSong');
    }
}
