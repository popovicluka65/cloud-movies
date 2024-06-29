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
}
