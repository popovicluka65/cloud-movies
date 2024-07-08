import { Component } from '@angular/core';
import {LayoutModule} from "./modules/layout/layout.module";
import {RouterOutlet} from "@angular/router";
import {MovieModule} from "./modules/movie/movie.module";
import {LoginComponent} from "./modules/auth/login/login.component";
import {SearchComponent} from "./modules/layout/search/search.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [
    LayoutModule,
    RouterOutlet,
    MovieModule,
    LoginComponent,
    SearchComponent,
  ],
  standalone: true
})
export class AppComponent {
  title = 'cloud-front';
}
