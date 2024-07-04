import {Component, Input, Output} from '@angular/core';
import {Router} from "@angular/router";
import EventEmitter from "events";
import {Movie} from "../../../models/movie";


@Component({
  selector: 'app-movie-card',
  templateUrl: './movie-card.component.html',
  styleUrl: './movie-card.component.css'
})
export class MovieCardComponent  {
  // @ts-ignore
  @Input() movie: Movie;
  // @ts-ignore
  @Output() clicked: EventEmitter<Movie> = new EventEmitter<Movie>();

  constructor(private router: Router) {
  }

  toDetails(id: string | undefined) {
    console.log(id)
    this.router.navigate(['/home', id+":"+this.movie.title!]);
  }
}
