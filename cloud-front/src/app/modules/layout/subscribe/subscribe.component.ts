import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import {MovieService} from "../../movie/movie.service";
import {AuthService} from "../../services/auth.service";
import {LayoutModule} from "../layout.module";
import {concatMap, delay, of, switchMap} from "rxjs";

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

  constructor(private movieService: MovieService, private authService: AuthService) {
    this.movieService.getSubscribeByUser(this.authService.getUsername()).pipe(
      switchMap(data => {
        console.log(data.data);
        this.searchResults = data.data;
        // Odloži izvršenje sledeće akcije za 2 sekunde
        return of(null).pipe(delay(2000));
      }),
      switchMap(() => this.movieService.interaction(this.authService.getUsername()))
    ).subscribe(
      (result: any) => {
        console.log(result);
      },
      (error) => {
        console.error('Greška prilikom dobavljanja filmova:', error);
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

    this.movieService.subscribe(searchData).pipe(
      switchMap((response) => {
        console.log('Subscribe response:', response);
        // Pozivamo interaction nakon što se subscribe završi
        return this.movieService.interaction(this.authService.getUsername());
      })
    ).subscribe(
      (result: any) => {
        console.log('Interaction result:', result);
      },
      (error) => {
        console.error('Greška prilikom interakcije ili pretplate:', error);
      }
    );
  }

  clearResults(id:string) {
    console.log("UDJE OVDE")
    // console.log(this.authService.getUsername())
    // this.movieService.deleteSubscribe(id,this.authService.getUsername()).subscribe(
    //   () => {
    //     console.log(`Subscription with ID ${id} deleted successfully.`);
    //     // Ažuriraj listu pretplata
    //     //this.loadSubscriptions();
    //   },
    //   error => {
    //     console.error('Error deleting subscription', error);
    //   }
    // );
    //
    // this.movieService.interaction(this.authService.getUsername()).subscribe(
    //   (result:any) => {
    //     console.log(result)
    //   },
    //   (error) => {
    //     console.error('Greška prilikom dobavljanja filmova:', error);
    //   }
    // );
    this.movieService.deleteSubscribe(id, this.authService.getUsername()).pipe(
      concatMap(() => {
        console.log(`Subscription with ID ${id} deleted successfully.`);
        // Ažuriraj listu pretplata
        // this.loadSubscriptions();
        // Odloži izvršenje sledeće akcije za 2 sekunde
        return of(null).pipe(delay(2000));
      }),
      concatMap(() => this.movieService.interaction(this.authService.getUsername()))
    ).subscribe(
      (result: any) => {
        console.log(result);
      },
      (error) => {
        console.error('Greška prilikom brisanja pretplate ili dobavljanja filmova:', error);
      }
    );
  }
}
