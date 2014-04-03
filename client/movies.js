function loadMovieList(searchQuery) {
  $.getJSON("http://localhost:8080/api/movies", {
    api_key: "75e821c10fe1bf8fc45ae3f2c008b7d1",
    search: searchQuery
  }).done(function (data) {
    displayMovieList(data.movies);
  });
}

function displayMovieList(movies) {
  var $movieList = $("#movie-list");
  $movieList.empty();
  $.each(movies, function (index, movie) {
    var $movie = $("<div></div>").addClass("movie");
    $movie.text(index + 1 + ": " + movie.name);
    $movie.appendTo($movieList);
    $movie.click(function () {
      loadMovieDetails(movie.id);
    });
  });
}

function loadMovieDetails(movieId) {
  $.getJSON("http://localhost:8080/api/movies/" + movieId, {
    api_key: "75e821c10fe1bf8fc45ae3f2c008b7d1"
  }).done(function (data) {
    displayMovieDetails(data);
  });
}

function displayMovieDetails(movie) {
  if (movie.poster_url) {
    var $posterImage = $("<img>").attr("src", movie.poster_url);
    $("#movie-poster").html($posterImage);
  } else {
    $("#movie-poster").empty();
  }

  $("#movie-title").text(movie.title);
  $("#movie-release").text("Released: " + movie.release_date);
  $("#movie-rating").text("Rating: " + movie.rating);

  $("#movie-details").show();
  $("#new-movie").hide();
}

function createMovie() {
  var movieData = $("#movie-form").serialize();
  $.post("http://localhost:8080/api/movies", movieData, function () {
    alert("Your movie was created! Try searching for it.");
  });
}

function displayNewMovieForm() {
  $("#movie-details").hide();
  $("#new-movie").show();
}

$(function () {
  $("#search-button").click(function () {
    var searchQuery = $("#search-field").val();
    loadMovieList(searchQuery);
  });

  $("#new-movie-button").click(function () {
    displayNewMovieForm();
  });

  $("#create-movie-button").click(function () {
    createMovie();
  });
});
