<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use League\Csv\Reader;
use League\Csv\Statement;

class SearchController extends Controller
{
    public function index(Request $request) {
        $query = \App\Song::with('topSong')->limit(intval($request->get('size')))
          ->whereBetween('topSimilarityPercentage', [
            intval($request->get('similarityMin')) / 100,
            intval($request->get('similarityMax')) / 100,
          ])->whereBetween('ngrams_matched', [
            intval($request->get('ngramsMin')),
            intval($request->get('ngramsMax'))
          ]);

        if ($request->get('rankingType') === "1") {
          $query = $query->orderBy('topSimilarityPercentage', 'DESC');
        }

        if ($request->get('rankingType') === "2") {
          $query = $query->orderBy('ngrams_matched', 'DESC');
        }

        if ($request->get('rankingType') === "3") {
          $query = $query->orderBy('averageRanking', 'ASC');
        }

        if ($request->get('rankingType') === "4") {
          $query = $query->orderBy('weightedAverageRanking', 'ASC');
        }

        return $query->get();
    }

    public function song(\App\Song $song) {
      return [
        "id" => $song->id,
        "artist" => $song->artist,
        "title" => $song->title,
        "lyrics" => $song->lyrics,
        "ngrams" => $song->ngrams->flatMap(function ($x) {
            return [$x->name => $x->popular_songs_count];
        }),
        "popularSongs" => $song->ngrams->flatMap(function ($x) {
            return $x->popularSongs->map(function ($y) {
              return [
                'title' => $y->title,
                'artist' => $y->artist
              ];
            });
        })->unique(),
      ];
    }

    public function insert() {
        ini_set('memory_limit', '4096M');
        ini_set('max_execution_time', 0);

        $this->insertTopSongs();

        $stream = fopen(storage_path('app/output.csv'), 'r');
        $csv = Reader::createFromStream($stream);
        $csv->setHeaderOffset(0);

        //build a statement
        $stmt = (new Statement());

        $topSongs = \App\TopSong::all()->mapWithKeys(function ($item) {
            return [$item->artist . ' - ' . $item->title => $item->id];
        });

        //query your records from the document
        $records = $stmt->process($csv);
        $start = microtime(true);
        $insertions = [];
        \DB::transaction(function () use ($records, $topSongs, $insertions) {
            foreach ($records as $record) {
                $song = \App\Song::create([
                  'ngrams_matched' => $record['nNgramsMatched'],
                  'artist' => $record['artist'],
                  'title' => $record['title'],
                  'lyrics' => $record['lyrics'],
                  'averageRanking' => $record['averageRanking'] === 'NaN' ? null : $record['averageRanking'],
                  'weightedAverageRanking' => $record['weightedAverageRanking'] === 'NaN' ? null : $record['weightedAverageRanking'],
                  'topSimilarityPercentage' => $record['topSimilarityPercentage'] === 'NaN' ? null : $record['topSimilarityPercentage'],
                  'top_song_id' => $topSongs[$record['topSimilaritySong']]
                ]);
            }
        });
        return microtime(true) - $start;
    }

    private function insertTopSongs() {
      $stream = fopen(storage_path('app/songs-lyrics-cleaned.csv'), 'r');
      $csv = Reader::createFromStream($stream);
      $csv->setHeaderOffset(0);

      //build a statement
      $stmt = (new Statement());

      //query your records from the document
      $records = $stmt->process($csv);
      \DB::transaction(function () use ($records) {
          foreach ($records as $record) {
              \App\TopSong::create([
                'artist' => $record['artist'],
                'title' => $record['title'],
                'lyrics' => $record['lyrics'],
                'rank' => $record['ranking'],
                'year' => $record['year'],
              ]);
          }
      });
    }

    public function find() {
      return \App\Song::where('title', 'Hot in Here')->get();
    }

    public function ngrams() {
      ini_set('memory_limit', '4096M');
      ini_set('max_execution_time', 0);
      return \App\Ngram::withCount('popularSongs')
        ->orderBy('popular_songs_count', 'desc')
        ->limit(200)
        ->get()
        ->flatMap(function ($x) {
        return [$x->name => intval($x->popular_songs_count / 10)];
      });
    }
}
