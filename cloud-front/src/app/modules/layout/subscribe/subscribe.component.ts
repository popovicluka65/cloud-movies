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
    this.movieService.getSubscribeByUser(this.authService.getUsername()).subscribe(
      data => {
        console.log(data.data)
        this.searchResults = data.data;
      },
      error => {
        console.error('Error fetching subscriptions', error);
      }
    );
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
    console.log(this.authService.getUsername())
    this.movieService.deleteSubscribe(id,this.authService.getUsername()).subscribe(
      () => {
        console.log(`Subscription with ID ${id} deleted successfully.`);
        // Ažuriraj listu pretplata
        //this.loadSubscriptions();
      },
      error => {
        console.error('Error deleting subscription', error);
      }
    );
  }
}
