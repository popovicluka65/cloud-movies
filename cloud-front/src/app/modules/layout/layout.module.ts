import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {NavbarComponent} from "./navbar/navbar.component";
import {RouterModule} from "@angular/router";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatButton} from "@angular/material/button";
import {MovieModule} from "../movie/movie.module";

@NgModule({
  declarations: [
    NavbarComponent
  ],
    imports: [
        CommonModule,
        RouterModule,
        FormsModule,
        ReactiveFormsModule,
        MatToolbarModule,
        MatButton,
    ],
  exports: [
    NavbarComponent,
  ]
})
export class LayoutModule { }
