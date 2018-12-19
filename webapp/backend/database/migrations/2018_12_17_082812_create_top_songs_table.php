<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateTopSongsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('top_songs', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            $table->string('artist');
            $table->string('title');
            $table->text('lyrics');
            $table->unsignedInteger('rank');
            $table->unsignedInteger('year');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('top_songs');
    }
}
