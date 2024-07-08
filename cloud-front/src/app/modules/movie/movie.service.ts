import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {BehaviorSubject, map, Observable} from "rxjs";
import {environment} from "../../environment/environment";
import {PersingedS3} from "../../models/persingedS3";
import {Movie} from "../../models/movie";


@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private movieList: Movie[] = [];
  private moviesSubject = new BehaviorSubject<Movie[]>([]);

  movies$ = this.moviesSubject.asObservable();

  constructor(private httpClient: HttpClient) {
    this.getMovies().subscribe({
      next: (data: Movie[]) => {
        this.moviesSubject.next(data);
        console.log(data);
      },
      error: (error) => {
        console.error("Greška pri dohvatanju filmova", error);
      }
    });
  }

  getMovie(title: string): Observable<Movie> {
    console.log(environment.apiHost + "getSingleMovie/" + title);
    const url = environment.apiHost + "getSingleMovie/" + title;
    return this.httpClient.get<Movie>(url);
  }

  getMovieFromS3(id: string): Observable<string> {
    console.log(environment.apiHost + "getFromS3/" + id);
    const url = environment.apiHost + "getFromS3/" + id;
    return this.httpClient.get(url, {responseType: 'text'});
  }

  getMovies(): Observable<Movie[]> {
    const url = environment.apiHost + "movies123";
    return this.httpClient.get<Movie[]>(url);
  }

  downloadRecord(downloadRecord: any): Observable<string> {
    const url = environment.apiHost + "downloadRecordUser";
    return this.httpClient.post(url, downloadRecord, {responseType: 'text'});
  }

  //dodati sta treba, ovo je samo template, proslediti sta treba, promeniti putanju i potencijalno return...
  uploadMovie(movieData: any): Observable<any> {
    const url = environment.apiHost+"movieS3";
    return this.httpClient.post(url, movieData);
    // .pipe(
    // map(response => response.persignedUrl) // Mapiramo odgovor da vratimo samo upload_url

  }

  editMovie(movieData: any): Observable<string> {
    const url = environment.apiHost + "putMovie";
    return this.httpClient.put(url, movieData, {responseType: 'text'});
  }

  uploadFileToS3(presignedUrl: string, file: File): Observable<string> {
    const headers = {
      'Content-Type': file.type
    };
    return this.httpClient.put<string>(presignedUrl, file, {responseType: 'json', headers});
  }

  transcodeMovie(id: any): Observable<any> {
    const url = environment.apiHost+"sendMessageTranscode";
    return this.httpClient.post(url, id);
    // .pipe(
    // map(response => response.persignedUrl) // Mapiramo odgovor da vratimo samo upload_url

  }

  subscribe(data: any): Observable<string> {
    console.log(data)
    const url = environment.apiHost + "subscribe";
    return this.httpClient.post<string>(url, data, {responseType: 'json'});
  }
  getFeed(username: string | null): Observable<Movie[]> {
    const url = `${environment.apiHost}feed/`+username;
    return this.httpClient.get<Movie[]>(url);
  }


  searchMovies(searchParams: any): Observable<any> {
    const url = environment.apiHost + "search";
    console.log(url)
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    return this.httpClient.post<any>(url, searchParams, {headers}).pipe(
      map(response => {
        // Ako je odgovor strukturiran kao vaš prethodno prikazani objekt
        if (response.COUNT && Array.isArray(response.COUNT)) {
          // @ts-ignore
          return response.COUNT.map(item => ({
            movie_id: item.movie_id,
            size: item.size,
            date_modified: item.date_modified,
            director: item.director,
            actors: item.actors,
            date_created: item.date_created,
            description: item.description,
            genres: item.genres,
            name: item.name,
            all_attributes: item.all_attributes,
            title: item.title,
            type: item.type
          })) as Movie[];
        } else {
          console.error('Neočekivan format odgovora');
          return [];
        }
      })
    );
  }

  updateMovies(searchedMovies: Movie[]) {
    this.moviesSubject.next(searchedMovies);
  }

  deleteSubscribe(id: string, username: string | null) {
    const url = `${environment.apiHost}unsubscribe/` + id+'++++'+username;
    return this.httpClient.delete(url);
  }

  addReview(username: string | null, rate: number, movieId: string, title: string) {
    const body = {
      username: username,
      rate: rate,
      movie_id: movieId,
      title: title
    };
    return this.httpClient.post(`${environment.apiHost}addReviewFunction`, body);
  }

  getSubscribeByUser(username: string | null): Observable<any> {
    const url = environment.apiHost + "getSubscribe/"+username;
    return this.httpClient.get<any>(url);
  }

  deleteMovie(movieId: string) {
    const url = `${environment.apiHost}deleteMovie/` + movieId;
    return this.httpClient.delete(url);
  }

  interaction(username: string | undefined | null): Observable<any> {
    console.log("UDJE U interaction")
    const url = `${environment.apiHost}interaction`;
    return this.httpClient.put<any>(url, { username });
  }

  getTranscodedVideo(data:any): Observable<any> {
    const url = `${environment.apiHost}transcoding`;
    return this.httpClient.post<any>(url,data );
  }
}
