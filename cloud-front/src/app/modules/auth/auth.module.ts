import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatInputModule} from "@angular/material/input";
import {MatRadioModule} from "@angular/material/radio";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatButtonModule} from "@angular/material/button";
import {RegisterComponent} from "./register/register.component";
import {LoginComponent} from "./login/login.component";



@NgModule({
  declarations: [
    // RegisterComponent,
    // LoginComponent,
  ],
  imports: [
    CommonModule,
    MatInputModule,
    MatRadioModule,
    FormsModule,
    MatButtonModule,
    ReactiveFormsModule
  ]
})
export class AuthModule { }
