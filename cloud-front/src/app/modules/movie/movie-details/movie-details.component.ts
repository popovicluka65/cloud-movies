import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MovieService} from "../movie.service";
import { HttpClient } from '@angular/common/http';
import {ActivatedRoute, Router} from "@angular/router";
import {Movie} from "../../../models/movie";
import {MatButton} from "@angular/material/button";
import {NgIf} from "@angular/common";
import {AuthService} from "../../services/auth.service";
import {LayoutModule} from "../../layout/layout.module";


@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [
    MatButton,
    NgIf,
    LayoutModule
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

  constructor(private movieService:MovieService,private http: HttpClient,private route: ActivatedRoute,
              private authService:AuthService, private router: Router) {
    console.log("ROLEEEE MOVIES")
    console.log(authService.getRole())
    this.role = authService.getRole();
    console.log(this.role);
    this.route.params.subscribe(params => {
      const id = params['movieId'];
      let lastIndex =  params['movieId'].lastIndexOf(':');
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
            let lastIndex =  params['movieId'].lastIndexOf(':');
            let id2 = params['movieId'].substring(0, lastIndex);
            let title = params['movieId'].substring(lastIndex + 1);
            this.movieId = id2;
            this.title = title

            this.getMovie();
        });
    }
  // ngAfterViewInit(): void {
  //     this.route.params.subscribe(params => {
  //         const id = params['movieId'];
  //         let lastIndex =  params['movieId'].lastIndexOf(':');
  //         let id2 = params['movieId'].substring(0, lastIndex);
  //         let title = params['movieId'].substring(lastIndex + 1);
  //         this.movieId = id2;
  //         this.title = title
  //
  //         this.getMovie();
  //     });
  //
  // }

  getMovie() {
    this.movieService.getMovie(this.movieId+":"+this.title).subscribe(
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

  download() {this.http.get(this.videoUrl, { responseType: 'blob' }).subscribe(
      (response: Blob) => {
        const blob = new Blob([response], { type: 'video/mp4' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = this.movie!.name!;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        let downloadRecord = {
            "userId": "popovicluka65@gmail.com",
            "movie_id": this.movie!.movie_id,
            "title": this.movie!.title
        }
        this.movieService.downloadRecord(downloadRecord).subscribe(
              (data) => {
                  console.log('Downloaded data:', data);
                  // Možete dalje obraditi preuzete podatke ovde
              },
              (error) => {
                  console.error('Error downloading data:', error);
              }
          );
      },
      (error) => {
        console.error('Error downloading video:', error);
        // Handle error
      }
    );
  }

  edit() {
    this.router.navigate(['/editMovie', this.movie!.movie_id+":"+this.movie!.title]);
  }

  delete() {

  }

  review(){

  }
}
