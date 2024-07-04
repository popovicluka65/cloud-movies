import {AfterViewInit, Component} from '@angular/core';
import {LayoutModule} from "../../layout/layout.module";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {Movie} from "../../../models/movie";
import {MovieService} from "../movie.service";
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";
import {FormArray, FormControl, FormGroup, FormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-edit-movie',
  standalone: true,
  imports: [
    LayoutModule,
    NgIf,
    FormsModule,
    NgForOf,
    NgClass
  ],
  templateUrl: './edit-movie.component.html',
  styleUrl: './edit-movie.component.css'
})
export class EditMovieComponent implements AfterViewInit {
  movieId: string = "";
  title2: string = "";
  movie: Movie | undefined;
  role: string | null = null;
  genreList: string[] = ['Action', 'Drama', 'Comedy', 'Horror', 'Sci-Fi'];
  description: string = '';
  director: string = '';
  actors: string = '';
  genres: string[] = [];
  title: string = '';
  videoUrl: string = '';
  movieFile: File | null = null;





  constructor(private movieService:MovieService,private http: HttpClient,private route:
    ActivatedRoute,private authService:AuthService, private router: Router) {
    console.log("ROLEEEE MOVIES")
    console.log(authService.getRole())
    this.role = authService.getRole();
    console.log(this.role);
  }
  ngAfterViewInit(): void {
    this.route.params.subscribe(params => {
      let lastIndex =  params['movieId'].lastIndexOf(':');
      this.title2 = params['movieId'].substring(lastIndex + 1);
      this.movieId = params['movieId'].substring(0, lastIndex);

      this.getMovie();


    })
  }
  getMovie() {
    this.movieService.getMovie(this.movieId+":"+this.title2).subscribe(
      (movie: Movie) => {
        console.log('Received movie:', movie);
        this.movie = movie;
        console.log("MOVIE")
        console.log(this.movie)
        this.description = this.movie.description!
        this.actors = this.movie.actors!
        this.director = this.movie.director!
        this.genres = this.movie.genres!
        this.title = this.movie.title!

        this.updateSelectedGenres();
      },
      error => {
        console.error('Error fetching movie:', error);
      }
    );
  }


  onFileChange(event: any) {
    this.movieFile = event.target.files[0];
  }

  updateSelectedGenres() {
    this.genres = [...this.genres];
  }

  isGenreSelected(genre: string): boolean {
    // console.log(this.genres)
    // console.log(genre)
    // console.log(this.genres.includes(genre))
    return this.genres.includes(genre);
  }

  onGenreChange(event: any) {
    const genre = event.target.value;
    if (event.target.checked) {
      this.genres.push(genre);
    } else {
      this.genres = this.genres.filter(g => g !== genre);
    }
  }

  onSubmit() {
    if (this.movieFile == null) {
      const movie = {
        id: this.movie?.movie_id,
        title: this.title,
        description: this.description,
        director: this.director,
        actors: this.actors,
        genres: this.genres,
        name: this.movie?.name,
        type: this.movie?.type,
        size: this.movie?.size!.toString(),
        dateModified: new Date(this.movie!.date_modified!).toISOString(),
        //dateCreated: new Date(this.movie.lastModified).toISOString()
        dateCreated: new Date(this.movie!.date_created!).toISOString()

      }
      this.movieService.uploadMovie(movie).subscribe(
        (response: string) => {
          console.log(response);
        },
        (error: any) => {
          console.error(error);

        }
      );
    } else {
      const editMovie = {
        id: this.movie?.movie_id,
        title: this.title,
        description: this.description,
        director: this.director,
        actors: this.actors,
        genres: this.genres,
        name: this.movieFile?.name,
        type: this.movieFile?.type,
        size: this.movieFile?.size.toString(),
        dateModified: new Date(this.movieFile!.lastModified).toISOString(),
        //dateCreated: new Date(this.movieFile!.lastModified).toISOString()
        dateCreated: new Date().toISOString()

      }
        this.movieService.uploadMovie(editMovie).subscribe(
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

          }
        );
    }

    this.router.navigate(['/home', this.movie?.movie_id+":"+this.movie?.title!])
  }

}
