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
import { AuthenticationDetails, CognitoUser, CognitoUserPool, CognitoUserSession, CognitoUserAttribute } from 'amazon-cognito-identity-js';
import {Router} from "@angular/router"; // Prilagodi putanju zavisno od bibliotekeimport {Router} from "@angular/router";
import * as jwtDecode from 'jwt-decode';
import {LayoutModule} from "../../layout/layout.module";
import {MovieService} from "../../movie/movie.service";
import {Movie} from "../../../models/movie";

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
    FormsModule,
    LayoutModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit{

  //gpt generisao
  loginUsername: string = "";
  loginPassword: string = "";
  userGroup: string = "";
  Role = "";

  private userPoolData = {
    UserPoolId: environment.userPoolId, // Zameni sa svojim User Pool ID
    ClientId: environment.userPoolClientId // Zameni sa svojim User Pool Client ID
  };

  private userPool = new CognitoUserPool(this.userPoolData);

  constructor(private router: Router,private authService:AuthService,private movieService:MovieService) {}

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
      onSuccess: (session: CognitoUserSession) => {
        console.log('Login successful:', session);

        // Dohvati informaciju o korisniku
        console.log(cognitoUser)
        cognitoUser.getUserAttributes((err, attributes) => {
          if (err) {
            console.error('Failed to fetch user attributes:', err);
            return;
          }

          const idToken = session.getIdToken().getJwtToken();
          //dobavi lepo
          console.log(idToken)
          localStorage.setItem('currentUser', idToken);
          console.log(this.loginUsername)
          this.router.navigate(['/home']);
          this.movieService.getFeed(this.loginUsername).subscribe(
            (movies:Movie[]) => {
              this.movieService.updateMovies(movies);
            },
            (error) => {
              console.error('Greška prilikom dobavljanja filmova:', error);
            }
          );
        });
      },
      onFailure: (err) => {
        console.error('Login failed:', err);
      },
    });
  }

}
