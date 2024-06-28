import {CUSTOM_ELEMENTS_SCHEMA, NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import {LayoutModule} from "./modules/layout/layout.module";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatIconModule} from "@angular/material/icon";
import {MovieModule} from "./modules/movie/movie.module";
import {AuthModule} from "./modules/auth/auth.module";
import {Amplify} from "aws-amplify";

import {AmplifyAuthenticatorModule} from "@aws-amplify/ui-angular";
import {Interceptor} from "./modules/auth/interceptor";
import {HTTP_INTERCEPTORS, HttpClient, HttpClientModule} from "@angular/common/http";

Amplify.configure({
  Auth: {
    Cognito: {
      identityPoolId: '',
      userPoolId: 'eu-central-1_rzNdae5DO',
      userPoolClientId: '1pqmkm01elhhmruf11383q6vu8',
      loginWith: {
         email: true,
      },
    },
  }
})

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
    MovieModule,
    AuthModule,
    AmplifyAuthenticatorModule

  ],
  providers: [

    {
      provide: HTTP_INTERCEPTORS,
      useClass: Interceptor,
      multi: true,
    }
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
