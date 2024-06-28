import {RouterModule, Routes} from '@angular/router';
import {NgModule,CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import {RegisterComponent} from "./modules/auth/register/register.component";
import {LoginComponent} from "./modules/auth/login/login.component";
import {MovieCardComponent} from "./modules/movie/movie-card/movie-card.component";
import {ConfirmEmailComponent} from "./modules/auth/confirm-email/confirm-email.component";

export const routes: Routes = [
  {path: '', redirectTo: 'movies', pathMatch: 'full'},
  {path: 'movies', component : MovieCardComponent},
  { path : 'login', component : LoginComponent},
  { path  : 'register', component : RegisterComponent},
  {path  : 'verify-email', component :  ConfirmEmailComponent}
];

