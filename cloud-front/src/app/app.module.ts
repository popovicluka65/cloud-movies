import {CUSTOM_ELEMENTS_SCHEMA, NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import {LayoutModule} from "./modules/layout/layout.module";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {MatIconModule} from "@angular/material/icon";
import {MovieModule} from "./modules/movie/movie.module";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    RouterModule,
    LayoutModule,
    BrowserAnimationsModule,
    MatIconModule,
    MovieModule

  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule { }
