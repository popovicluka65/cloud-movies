import {RouterModule, Routes} from '@angular/router';
import {NgModule,CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import {RegisterComponent} from "./modules/auth/register/register.component";
import {LoginComponent} from "./modules/auth/login/login.component";
import {MovieCardComponent} from "./modules/movie/movie-card/movie-card.component";
import {ConfirmEmailComponent} from "./modules/auth/confirm-email/confirm-email.component";
import {MovieDetailsComponent} from "./modules/movie/movie-details/movie-details.component";

export const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: 'home', component : MovieCardComponent},
  { path : 'login', component : LoginComponent},
  { path  : 'register', component : RegisterComponent},
  {path  : 'verify-email', component :  ConfirmEmailComponent},
  {component:MovieDetailsComponent, path:"home/:movieId"}
];

