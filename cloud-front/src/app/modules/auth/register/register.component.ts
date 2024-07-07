import {Component, OnInit} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatRadioButton, MatRadioGroup} from "@angular/material/radio";
import {MatButton} from "@angular/material/button";
import {MatFormField} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {MatToolbar} from "@angular/material/toolbar";
import {MatCard} from "@angular/material/card";
import {CognitoUser, CognitoUserAttribute, CognitoUserPool} from "amazon-cognito-identity-js";
import {Router} from "@angular/router";
import {environment} from "../../../environment/environment";
import AWS from 'aws-sdk';
import {LayoutModule} from "../../layout/layout.module";
import {HttpClient} from "@angular/common/http";

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
    FormsModule,
    LayoutModule
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})

export class RegisterComponent implements OnInit {


  registerUsername: string = "";
  registerPassword: string = "";
  registerEmail: string = "";
  registerGivenName: string = "";
  registerFamilyName: string = "";
  registerBirthdate: string = "";

  private userPoolData = {
    UserPoolId: environment.userPoolId, // Zameni sa svojim User Pool ID
    ClientId: environment.userPoolClientId // Zameni sa svojim Client ID
  };



  private userPool = new CognitoUserPool(this.userPoolData);

  constructor(private router: Router,private httpClient:HttpClient) {}

  ngOnInit(): void {}

  onRegister() {

    const emailAttribute = {
      Name: 'email',
      Value: this.registerEmail
    };
    const givenNameAttribute = {
      Name: 'given_name',
      Value: this.registerGivenName
    };
    const familyNameAttribute = {
      Name: 'family_name',
      Value: this.registerFamilyName
    };
    const birthdateAttribute = {
      Name: 'birthdate',
      Value: this.registerBirthdate
    };

    const attributeList: CognitoUserAttribute[] = [];
    attributeList.push(new CognitoUserAttribute(emailAttribute));
    attributeList.push(new CognitoUserAttribute(givenNameAttribute));
    attributeList.push(new CognitoUserAttribute(familyNameAttribute));
    attributeList.push(new CognitoUserAttribute(birthdateAttribute));

    this.userPool.signUp(this.registerUsername, this.registerPassword,attributeList, [], (err, result) => {
      if (err) {
        console.error('Registration failed:', err);
        return;
      }

      console.log('Registration successful:', result);
      console.log(result?.userSub)
      this.addUserToGroup(result?.userSub,this.registerPassword).subscribe(
        response => {
          console.log('User added to group:', response);
        },
        error => {
          console.error('Failed to add user to group:', error);
        }
      );
      this.router.navigate(['/verify-email/'+this.registerUsername]); // Zameni sa putanjom na koju želiš da preusmeriš korisnika nakon registracije
    });
  }

  addUserToGroup(username: string | undefined, password: string){
    const data = {
      username:username,
      //password: password,
    };
    const url = environment.apiHost+"toGroup";
    console.log(url)
    console.log(data)
    return this.httpClient.post(url, data, { responseType: 'json' });
  }

}
