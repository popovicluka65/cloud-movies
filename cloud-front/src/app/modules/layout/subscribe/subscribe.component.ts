import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import {MovieService} from "../../movie/movie.service";
import {AuthService} from "../../services/auth.service";
import {LayoutModule} from "../layout.module";

@Component({
  selector: 'app-subscribe',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    NgIf,
    LayoutModule
  ],
  templateUrl: './subscribe.component.html',
  styleUrl: './subscribe.component.css'
})
export class SubscribeComponent {
  selectedCriteria: string = '';
  searchQuery: string = '';
  searchOptions: string[] = ['Genre', 'Director', 'Actor'];
  searchResults: any[] = [];

  constructor(private movieService:MovieService,private authService:AuthService) {
    this.searchResults = [
      { id:"1", type: 'Type 1', contentCreator: 'Creator 1' },
      { id:"2",type: 'Type 2', contentCreator: 'Creator 2' },
      { id:"3",type: 'Type 3', contentCreator: 'Creator 3' }
    ];
  }
  performSearch() {
    console.log(`Searching for ${this.searchQuery} by ${this.selectedCriteria}`);
    const searchData = {
      subscriber:this.authService.getUsername(),
      email:this.authService.getEmail(),
      query: this.searchQuery,
      content: this.selectedCriteria
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

  clearResults(id:string) {
    console.log("DELETE")
    console.log(id)
    this.movieService.deleteSubscribe(id);
  }
}
