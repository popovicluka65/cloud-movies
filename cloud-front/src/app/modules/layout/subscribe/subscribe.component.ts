import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {MovieService} from "../../movie/movie.service";

@Component({
  selector: 'app-subscribe',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf
  ],
  templateUrl: './subscribe.component.html',
  styleUrl: './subscribe.component.css'
})
export class SubscribeComponent {
  selectedCriteria: string = '';
  searchQuery: string = '';
  searchOptions: string[] = ['Genre', 'Director', 'Actor'];

  constructor(private movieService:MovieService) {
  }
  performSearch() {
    console.log(`Searching for ${this.searchQuery} by ${this.selectedCriteria}`);
    const searchData = {
      searchQuery: this.searchQuery,
      selectedCriteria: this.selectedCriteria
    };

    this.movieService.subscribe(searchData)
      .subscribe(
        (response) => {
          console.log('Subscribe response:', response);
        },
        (error) => {
          console.error('Error subscribing:', error);
        }
      );
  }
}
