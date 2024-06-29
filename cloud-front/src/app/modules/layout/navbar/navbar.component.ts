import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {Observable} from "rxjs";
import {MovieService} from "../../movie/movie.service";
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent{
  constructor(private router: Router,private movieService:MovieService) {
  }
  Login() {
    this.router.navigate(['/login']);
  }

  Signup() {
    this.router.navigate(['/register']);
  }

  getMovie() {
    this.movieService.getMovie("Juzni vetar").subscribe(
      (movie: string) => {
        console.log('Received movie:', movie);

      },
      (error) => {
        console.error('Error fetching movie:', error);
        // Handle error
      }
    );
  }
}
