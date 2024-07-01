import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {MovieService} from "../movie.service";

@Component({
  selector: 'app-upload-movie',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf
  ],
  templateUrl: './upload-movie.component.html',
  styleUrl: './upload-movie.component.css'
})
export class UploadMovieComponent {
  title: string = '';
  description: string = '';
  director: string = '';
  actors: string = '';
  genres: string[] = [];
  movieFile: File | null = null;

  genreList: string[] = ['Action', 'Drama', 'Comedy', 'Horror', 'Sci-Fi'];

  constructor(private movieService:MovieService) {
  }

  onGenreChange(event: any) {
    const genre = event.target.value;
    if (event.target.checked) {
      this.genres.push(genre);
    } else {
      this.genres = this.genres.filter(g => g !== genre);
    }
  }

  onFileChange(event: any) {
    this.movieFile = event.target.files[0];
  }

  onSubmit() {
    const movie = {
      title: this.title,
      description: this.description,
      director: this.director,
      actors: this.actors,
      genres: this.genres,
      file: this.movieFile
    };
    console.log(movie);
    // Add your form submission logic here
    const uploadMovie = {
      title: this.title,
      description: this.description,
      director: this.director,
      actors: this.actors,
      genres: this.genres,
      name: this.movieFile?.name,
      type: this.movieFile?.type,
      size: this.movieFile?.size,
      dateModified: this.movieFile?.lastModified,
      dateCreated: this.movieFile?.lastModified
    }
    console.log(uploadMovie)

    this.movieService.uploadMovie(uploadMovie).subscribe(
      (response: string) => {
        console.log(response);
        this.movieService.uploadFileToS3(response, this.movieFile!).subscribe(
          (response: string) => {
            console.log(response);
          },
          (error: any) => {
            console.error(error);

          }
        );
      },
      (error: any) => {
        console.error(error);
        // Handle error response
      }
    );
  }
}
