import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MovieService} from "../movie.service";
import { HttpClient } from '@angular/common/http';
import {ActivatedRoute, Router} from "@angular/router";
import {Movie} from "../../../models/movie";


@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent implements AfterViewInit{

  @ViewChild('videoPlayer') videoPlayer!: ElementRef;
  videoUrl: string = '';
  movieId: string = "";
  title: string = "";
  movie: Movie | undefined;

  constructor(private movieService:MovieService,private http: HttpClient,private route: ActivatedRoute) {}
  ngAfterViewInit(): void {
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

  getMovie() {
    this.movieService.getMovie(this.movieId+":"+this.title).subscribe(
      (movie: Movie) => {
        console.log('Received movie:', movie);
        this.movie = movie;
        
        // this.playVideo();
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
        a.download = 'inception.mp4';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      },
      (error) => {
        console.error('Error downloading video:', error);
        // Handle error
      }
    );
  }

  edit() {

  }

  delete() {

  }
}
