import { Component } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatFormField, MatInput} from "@angular/material/input";
import {MatCheckbox} from "@angular/material/checkbox";
import {MatButton} from "@angular/material/button";
import {MatDatepickerToggle, MatDateRangeInput, MatDateRangePicker} from "@angular/material/datepicker";
import {MatToolbar} from "@angular/material/toolbar";
import {NgForOf} from "@angular/common";
import {MovieService} from "../../movie/movie.service";
import {Movie} from "../../../models/movie";

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    FormsModule,
    MatInput,
    MatFormField,
    MatCheckbox,
    MatButton,
    MatDateRangePicker,
    MatDatepickerToggle,
    MatDateRangeInput,
    ReactiveFormsModule,
    MatToolbar,
    NgForOf
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  searchOptions: string[] = ['Title', 'Description', 'Director', 'Actors', 'Genres'];
  searchQueries: string[] = this.searchOptions.map(() => '');
  searchedMovies : Movie[] = []

  constructor(private movieService:MovieService) {
  }

  performSearch() {
    const searchParams = this.searchOptions.reduce((params, option, index) => {
      if (option === 'Genres') {
        params[option.toLowerCase()] = this.searchQueries[index].split(',').map(value => value.trim());
      } else {
        params[option.toLowerCase()] = this.searchQueries[index];
      }
      return params;
    }, {} as { [key: string]: any });

    // For now, log the search parameters to the console
    console.log('Search Parameters:', searchParams);
    this.movieService.searchMovies(searchParams).subscribe(
      (results:any[]) => {
        console.log('Search Results:', results);
        // Handle the search results here
        this.searchedMovies = results;
        console.log("AAAA")
        console.log(this.searchedMovies)

      },
      (error) => {-+


        console.error('Search Error:', error);
        // Handle the error here
      }
    );
  }
}
