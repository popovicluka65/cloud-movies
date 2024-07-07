import { Component, OnInit } from '@angular/core';
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatButtonModule } from "@angular/material/button";
import { CognitoUser, CognitoUserPool } from "amazon-cognito-identity-js";
import { ActivatedRoute, Router } from "@angular/router";
import { environment } from "../../../environment/environment";
import { FormsModule } from "@angular/forms";
import { MatInputModule } from "@angular/material/input";
import AWS, {CognitoIdentityServiceProvider} from "aws-sdk";
import { LayoutModule } from "../../layout/layout.module";

AWS.config.region = 'eu-central-1'; // Postavite vaš region ovde
// AWS.config.credentials = new AWS.CognitoIdentityCredentials({
//   IdentityPoolId: 'eu-central-1' ,
//   // AccessKeyId: 'Active - AKIA6ODU7KB4H5BTGHOC',
//   // SecretAccessKey: 'your-secret-access-key'
// });

@Component({
  selector: 'app-confirm-email',
  standalone: true,
  templateUrl: './confirm-email.component.html',
  styleUrls: ['./confirm-email.component.css'],
  imports: [
    MatFormFieldModule,
    MatButtonModule,
    FormsModule,
    MatInputModule,
    LayoutModule
  ]
})


export class ConfirmEmailComponent implements OnInit {
  confirmationCode: string = "";
  username: string = "";
  message:string ="";

  constructor(private router: Router, private route: ActivatedRoute) {}

  private userPoolData = {
    UserPoolId: environment.userPoolId, // Zameni sa svojim User Pool ID
    ClientId: environment.userPoolClientId // Zameni sa svojim Client ID
  };

  private userPool = new CognitoUserPool(this.userPoolData);

  ngOnInit(): void {
    // Preuzimanje parametara iz URL-a, ako je potrebno
    this.route.params.subscribe(params => {
      this.username = params['username']; // Dobavljanje vrednosti parametra "username"
      console.log("Username:", this.username); // Možete dodati ovde konzolu da proverite da li se vrednost dobija
    });
  }

  confirmRegistration() {
    const userData = {
      Username: this.username,
      Pool: this.userPool
    };

    const cognitoUser = new CognitoUser(userData);

    cognitoUser.confirmRegistration(this.confirmationCode, true, (err, result) => {
      if (err) {
        console.error('Confirmation failed:', err);
        return;
      }
      console.log('Confirmation successful:', result);
      this.router.navigate(['/login']); // Redirekcija na stranicu za prijavljivanje nakon uspešne potvrde
    });
  }
}
