import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../environment/environment";
import {PersingedS3} from "../../models/persingedS3";


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
    const url = environment.apiHost+"movieS3";
    return this.httpClient.post(url, movieData, { responseType: 'text' });
      // .pipe(
      // map(response => response.persignedUrl) // Mapiramo odgovor da vratimo samo upload_url

  }

  uploadFileToS3(presignedUrl: string, file: File): Observable<string> {
    const headers = {
      'Content-Type': file.type
    };
    return this.httpClient.put<string>(presignedUrl, file,  { responseType: 'json',headers });
  }

  subscribe(data: any): Observable<string> {
    const url = environment.apiHost+"subscribe";
    return this.httpClient.post<string>(url, data, { responseType: 'json' });
  }


}
