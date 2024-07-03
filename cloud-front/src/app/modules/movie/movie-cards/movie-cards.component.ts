import {Component, OnInit} from '@angular/core';
import {Movie} from "../../../models/movie";
import {NgForOf} from "@angular/common";
import {MovieModule} from "../movie.module";
import {Router} from "@angular/router";
import {MovieService} from "../movie.service";
import {SearchComponent} from "../../layout/search/search.component";
import {LayoutModule} from "../../layout/layout.module";


@Component({
  selector: 'app-movie-cards',
  standalone: true,
  imports: [
    NgForOf,
    MovieModule,
    SearchComponent,
    LayoutModule
  ],
  templateUrl: './movie-cards.component.html',
  styleUrl: './movie-cards.component.css'
})
export class MovieCardsComponent implements  OnInit {

  movies: Movie[] = [];

    constructor(private movieService: MovieService) {
    }
  ngOnInit(): void {
    console.log("cao")
    this.loadMovies();


  }

  loadMovies(): void {
    this.movieService.getMovies().subscribe(
      (movies) => {
        this.movies = movies;
          console.log(this.movies)

      },
      (error) => {
        // console.error('Error fetching movies', error);
      }
    );
  }

}
