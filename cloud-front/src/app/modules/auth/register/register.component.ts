import {Component, OnInit} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatRadioButton, MatRadioGroup} from "@angular/material/radio";
import {MatButton} from "@angular/material/button";
import {MatFormField} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {MatToolbar} from "@angular/material/toolbar";
import {MatCard} from "@angular/material/card";
import {CognitoUserAttribute, CognitoUserPool} from "amazon-cognito-identity-js";
import {Router} from "@angular/router";
import {environment} from "../../../environment/environment";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatRadioGroup,
    MatRadioButton,
    MatButton,
    MatFormField,
    MatInput,
    MatToolbar,
    MatCard,
    FormsModule
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})

export class RegisterComponent implements OnInit {


  registerUsername: string = "";
  registerPassword: string = "";
  registerEmail: string = "";

  private userPoolData = {
    UserPoolId: environment.userPoolId, // Zameni sa svojim User Pool ID
    ClientId: environment.userPoolClientId // Zameni sa svojim Client ID
  };



  private userPool = new CognitoUserPool(this.userPoolData);

  constructor(private router: Router) {}

  ngOnInit(): void {}

  onRegister() {

    const emailAttribute = {
      Name: 'email',
      Value: this.registerEmail
    };
    const givenNameAttribute = {
      Name: 'given_name',
      Value: 'John'
    };
    const familyNameAttribute = {
      Name: 'family_name',
      Value: 'Doe'
    };

    const attributeList: CognitoUserAttribute[] = [];
    attributeList.push(new CognitoUserAttribute(emailAttribute));
    attributeList.push(new CognitoUserAttribute(givenNameAttribute));
    attributeList.push(new CognitoUserAttribute(familyNameAttribute));

    this.userPool.signUp(this.registerUsername, this.registerPassword,attributeList, [], (err, result) => {
      if (err) {
        console.error('Registration failed:', err);
        return;
      }
      console.log('Registration successful:', result);
      this.router.navigate(['/verify-email']); // Zameni sa putanjom na koju želiš da preusmeriš korisnika nakon registracije
    });
  }
}
