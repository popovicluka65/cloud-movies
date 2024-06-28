import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatButton} from "@angular/material/button";
import {MatCard} from "@angular/material/card";
import {MatFormField} from "@angular/material/form-field";
import {MatToolbar} from "@angular/material/toolbar";
import {MatInput} from "@angular/material/input";
import {AmplifyAuthenticatorModule} from "@aws-amplify/ui-angular";
import {AuthService} from "../../services/auth.service";
import {environment} from "../../../environment/environment";
import { CognitoUserPool, AuthenticationDetails, CognitoUser } from 'amazon-cognito-identity-js';
import {Router} from "@angular/router";


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
    AmplifyAuthenticatorModule,
    FormsModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit{

  //gpt generisao
  loginUsername: string = "";
  loginPassword: string = "";

  private userPoolData = {
    UserPoolId: environment.userPoolId, // Zameni sa svojim User Pool ID
    ClientId: environment.userPoolClientId // Zameni sa svojim User Pool Client ID
  };

  private userPool = new CognitoUserPool(this.userPoolData);

  constructor(private router: Router) {}

  ngOnInit(): void {}

  onLogin() {
    const authenticationData = {
      Username: this.loginUsername,
      Password: this.loginPassword,
    };
    const authenticationDetails = new AuthenticationDetails(authenticationData);

    const userData = {
      Username: this.loginUsername,
      Pool: this.userPool,
    };
    const cognitoUser = new CognitoUser(userData);

    cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: (result) => {
        console.log('Login successful:', result);
        this.router.navigate(['/home']); // Zameni sa putanjom na koju želiš da preusmeriš korisnika nakon prijave
      },
      onFailure: (err) => {
        console.error('Login failed:', err);
      },
    });
  }

}
