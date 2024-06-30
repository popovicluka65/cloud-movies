import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environment/environment";

@Injectable({
  providedIn: 'root'
})
export class MovieService {

  constructor(private httpClient:HttpClient) { }

  getMovie(title: string): Observable<string> {
    console.log(environment.apiHost+"getFromS3/"+title);
    const url = environment.apiHost+"getFromS3/"+title;
    return this.httpClient.get(url, { responseType: 'text' });
  }

  //dodati sta treba, ovo je samo template, proslediti sta treba, promeniti putanju i potencijalno return...
  uploadMovie(movieData: any): Observable<string> {
    const url = environment.apiHost+"getFromS3";
    return this.httpClient.post<string>(url, movieData, { responseType: 'text' as 'json' });
  }
  subscribe(data: any): Observable<string> {
    const url = environment.apiHost+"subscribe";
    return this.httpClient.post<string>(url, data, { responseType: 'json' });
  }
}
