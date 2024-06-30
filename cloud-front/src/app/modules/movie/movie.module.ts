import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MovieCardComponent} from "./movie-card/movie-card.component";
import {SearchComponent} from "../layout/search/search.component";



@NgModule({
  declarations: [
    MovieCardComponent,

  ],
    imports: [
        CommonModule,
        SearchComponent
    ],
  exports:[
    MovieCardComponent
  ]
})
export class MovieModule { }
