import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {Observable} from "rxjs";
import {MovieService} from "../../movie/movie.service";
import {AuthService} from "../../services/auth.service";
import {Movie} from "../../../models/movie";
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent{
  role: string | null = null;
  constructor(private router: Router,private movieService:MovieService,private authService:AuthService) {
    this.role = authService.getRole();
  }
  Login() {
    this.router.navigate(['/login']);
  }

  Signup() {
    this.router.navigate(['/register']);
  }

  toHome() {
    this.movieService.getFeed(this.authService.getUsername()).subscribe(
      (result: Movie[]) => {
        console.log(result);
        this.movieService.updateMovies(result);
      },
      (error) => {
        console.error('Greška prilikom dobavljanja filmova:', error);
      }
    );
    this.router.navigate(['/home']);
  }
  UploadVideo() {
    this.router.navigate(['/upload']);
  }
  Subscribe() {
    this.router.navigate(['/subscribe']);
  }

  //proveriti radi li
  SignOut() {
    localStorage.removeItem('currentUser');
    this.router.navigate(['/login']);
  }
}
