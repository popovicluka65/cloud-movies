import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatButton} from "@angular/material/button";
import {MatCard} from "@angular/material/card";
import {MatFormField} from "@angular/material/form-field";
import {MatToolbar} from "@angular/material/toolbar";
import {MatInput} from "@angular/material/input";
import {AmplifyAuthenticatorModule} from "@aws-amplify/ui-angular";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButton,
    MatCard,
    MatFormField,
    MatToolbar,
    MatInput,
    AmplifyAuthenticatorModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit{

  formFields = {
    signUp:{
      name:{
        order:1
      }
    },
    email:{
      name:{
        order:2
      }
    },
    password:{
      name:{
        order:3
      }
    },
    confirm_password:{
      name:{
        order:4
      }
    }
  }

  constructor(private authService:AuthService) {
  }

  async ngOnInit(): Promise<void> {
    let user = this.authService.getCurrentUser();
    console.log("PORUKA");
    console.log(user);
    console.log("PORUKA");
  }
}
