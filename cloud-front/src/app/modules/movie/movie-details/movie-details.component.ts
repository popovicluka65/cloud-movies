import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MovieService} from "../movie.service";
import { HttpClient } from '@angular/common/http';
import {ActivatedRoute, Router} from "@angular/router";
import {Movie} from "../../../models/movie";
import {MatButton} from "@angular/material/button";
import {NgIf} from "@angular/common";
import {AuthService} from "../../services/auth.service";
import {LayoutModule} from "../../layout/layout.module";
import {FormsModule} from "@angular/forms";
import {concatMap, mergeMap} from "rxjs";


@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [
    MatButton,
    NgIf,
    LayoutModule,
    FormsModule
  ],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent implements OnInit {

  @ViewChild('videoPlayer') videoPlayer!: ElementRef;
  videoUrl: string = '';
  movieId: string = "";
  title: string = "";
  movie: Movie | undefined;
  role: string | null = null;
  selectedRating: number = 0;
  selectedResolution: any = '';

  constructor(private movieService: MovieService, private http: HttpClient, private route: ActivatedRoute,
              private authService: AuthService, private router: Router) {
    this.role = authService.getRole();
    this.route.params.subscribe(params => {
      const id = params['movieId'];
      let lastIndex = params['movieId'].lastIndexOf(':');
      let id2 = params['movieId'].substring(0, lastIndex);
      let title = params['movieId'].substring(lastIndex + 1);
      this.movieId = id2;
      this.title = title

      this.getMovie();
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['movieId'];
      let lastIndex = params['movieId'].lastIndexOf(':');
      let id2 = params['movieId'].substring(0, lastIndex);
      let title = params['movieId'].substring(lastIndex + 1);
      this.movieId = id2;
      this.title = title

      this.getMovie();
    });
  }
  getMovie() {
    this.movieService.getMovie(this.movieId + ":" + this.title).subscribe(
      (movie: Movie) => {
        console.log('Received movie:', movie);
        this.movie = movie;
        this.movieService.getMovieFromS3(this.movieId).subscribe(
          (data) => {
            this.videoUrl = data;
            console.log('Movie data:', this.videoUrl);
            this.playVideo()

          },
          (error) => {
            console.error('Error fetching movie data:', error);
          }
        );

      },
      (error) => {
        console.error('Error fetching movie:', error);
      }
    );
  }

  playVideo() {
    const videoElement = this.videoPlayer.nativeElement;
    videoElement.src = this.videoUrl;
    videoElement.load();
    videoElement.play();
  }

  download() {
    this.http.get(this.videoUrl, { responseType: 'blob' }).pipe(
      mergeMap((response: Blob) => {
        const blob = new Blob([response], { type: 'video/mp4' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = this.movie!.name!;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        console.log('Video preuzet i preuzimanje započeto.');

        let downloadRecord = {
          "userId": this.authService.getUsername(),
          "movie_id": this.movie!.movie_id,
          "title": this.movie!.title
        };

        return this.movieService.downloadRecord(downloadRecord);
      }),
      concatMap((data) => {
        console.log('Preuzimanje zabeleženo:', data);
        // Možete dalje obraditi preuzete podatke ovde
        console.log("Započinjanje interakcije...");
        return this.movieService.interaction(this.authService.getUsername());
      })
    ).subscribe(
      (result: any) => {
        console.log('Interakcija uspešna:', result);
      },
      (error) => {
        console.error('Greška prilikom preuzimanja videa ili dobavljanja filmova:', error);
      }
    );
  }




  edit() {
    this.router.navigate(['/editMovie', this.movie!.movie_id + ":" + this.movie!.title]);
  }

  delete() {
    this.movieService.deleteMovie(this.movieId).subscribe(
      () => {
        console.log(`Deleted movie.`);
        this.router.navigate(['/home']);
      },
      error => {
        console.error('Error deleting movie', error);
      }
    );
  }
  rateContent(): void {
    // Implementacija funkcije za ocenjivanje sadržaja
    if (this.selectedRating) {
      console.log(`Ocenili ste sadržaj sa ${this.selectedRating} zvezdica.`);
      // Dodajte logiku za slanje ocene na server ili neki drugi postupak za čuvanje ocene
    } else {
      console.log('Molimo izaberite ocenu pre nego što ocenite sadržaj.');
    }

    this.movieService.addReview(this.authService.getUsername(), this.selectedRating, this.movieId, this.title)
      .pipe(
        concatMap(response => {
          console.log('Review added successfully:', response);
          // Nakon što je prva operacija uspešno završena, pozivamo drugu operaciju
          return this.movieService.interaction(this.authService.getUsername());
        })
      )
      .subscribe(
        (result: any) => {
          console.log(result);
        },
        (error) => {
          console.error('Greška prilikom dodavanja recenzije ili dobavljanja filmova:', error);
        }
      );
  }
  transcoding() {
    if (this.selectedResolution) {
      console.log(`${this.selectedResolution}`);
      const resolution: any = [];
      console.log(this.selectedResolution);

      if (this.selectedResolution === '360') {
        resolution.push(640, 360);
      } else if (this.selectedResolution === '480') {
        resolution.push(854, 480);
      } else if (this.selectedResolution === '720') {
        resolution.push(1280, 720);
      }
      const url_movie = "resized_["+resolution[0]+", "+resolution[1]+"]_"+this.movieId;
      const data = {
        "movie_id": url_movie
      }

      this.movieService.getTranscodedVideo(data).subscribe(
        (result: any) => {
          this.videoUrl = result.response;
          this.playVideo()
        },
        (error) => {
          console.error('', error);
        }
      );

    }
  }
}
