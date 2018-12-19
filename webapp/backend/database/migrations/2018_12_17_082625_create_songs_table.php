<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateSongsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('songs', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            $table->unsignedInteger('ngrams_matched');
            $table->string('artist');
            $table->string('title');
            $table->text('lyrics');
            $table->double('averageRanking')->nullable();
            $table->double('weightedAverageRanking')->nullable();
            $table->double('topSimilarityPercentage')->nullable();
            $table->unsignedInteger('top_song_id');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('songs');
    }
}
