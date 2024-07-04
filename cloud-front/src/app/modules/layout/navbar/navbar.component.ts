import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {Observable} from "rxjs";
import {MovieService} from "../../movie/movie.service";
import {AuthService} from "../../services/auth.service";
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent{
  role: string | null = null;
  constructor(private router: Router,private movieService:MovieService,private authService:AuthService) {
    console.log("ROLEEEE")
    console.log(authService.getRole())
    this.role = authService.getRole();
    console.log(this.role);
  }
  Login() {
    this.router.navigate(['/login']);
  }

  Signup() {
    this.router.navigate(['/register']);
  }

  // getMovie() {
  //   this.movieService.getMovie("Juzni vetar").subscribe(
  //     (movie: string) => {
  //       console.log('Received movie:', movie);
  //     },
  //     (error) => {
  //       console.error('Error fetching movie:', error);
  //       // Handle error
  //     }
  //   );
  // }
  toHome() {
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
