import {RouterModule, Routes} from '@angular/router';
import {NgModule,CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import {RegisterComponent} from "./modules/auth/register/register.component";
import {LoginComponent} from "./modules/auth/login/login.component";
import {MovieCardComponent} from "./modules/movie/movie-card/movie-card.component";
import {ConfirmEmailComponent} from "./modules/auth/confirm-email/confirm-email.component";
import {MovieDetailsComponent} from "./modules/movie/movie-details/movie-details.component";
import {UploadMovieComponent} from "./modules/movie/upload-movie/upload-movie.component";
import {SubscribeComponent} from "./modules/layout/subscribe/subscribe.component";
import {MovieCardsComponent} from "./modules/movie/movie-cards/movie-cards.component";
import {EditMovieComponent} from "./modules/movie/edit-movie/edit-movie.component";

export const routes: Routes = [
  {path : '', redirectTo: 'home', pathMatch: 'full'},
  {path : 'home', component : MovieCardsComponent},
  { path : 'login', component : LoginComponent},
  { path  : 'register', component : RegisterComponent},
  {path  : 'verify-email/:username', component :  ConfirmEmailComponent},
  {path : "home/:movieId", component:MovieDetailsComponent},
  {path  : 'upload', component : UploadMovieComponent},
  {path  : 'subscribe', component : SubscribeComponent },
  {path : 'editMovie/:movieId', component: EditMovieComponent}

];

