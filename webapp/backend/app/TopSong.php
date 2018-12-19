<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class TopSong extends Model
{
    protected $fillable = ['artist', 'title', 'lyrics', 'rank', 'year'];
}
