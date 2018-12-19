<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::fallback(function () {
    return File::get(public_path('index.html'));
});

// Route::get('/insert', 'SearchController@insert');
// Route::get('/ngrams', 'SearchController@ngrams');
// Route::get('/find', 'SearchController@find');

Route::middleware('cors')->get('/ws/search', 'SearchController@index');
Route::middleware('cors')->get('/ws/song/{song}', 'SearchController@song');
