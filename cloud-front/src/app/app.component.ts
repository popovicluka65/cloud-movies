import { Component } from '@angular/core';
import {LayoutModule} from "./modules/layout/layout.module";
import {RouterOutlet} from "@angular/router";
import {MovieModule} from "./modules/movie/movie.module";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [
    LayoutModule,
    RouterOutlet,
    MovieModule
  ],
  standalone: true
})
export class AppComponent {
  title = 'cloud-front';
}
