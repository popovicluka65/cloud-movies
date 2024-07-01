import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MovieService} from "../movie.service";
import { HttpClient } from '@angular/common/http';
import {ActivatedRoute, Router} from "@angular/router";


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

  constructor(private movieService:MovieService,private http: HttpClient,private route: ActivatedRoute) {}
  ngAfterViewInit(): void {
      this.route.params.subscribe(params => {
          const id = params['movieId'];
          this.movieId = id;
          this.getMovie();
      });

  }

  getMovie() {
    this.movieService.getMovie(this.movieId).subscribe(
      (movie: string) => {
        console.log('Received movie:', movie);
        this.videoUrl = movie;
        this.playVideo();
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
