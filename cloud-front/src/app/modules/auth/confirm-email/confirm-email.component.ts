import {Component, OnInit} from '@angular/core';
import {MatFormField} from "@angular/material/form-field";
import {MatButton} from "@angular/material/button";
import {message} from "@aws-amplify/ui/dist/types/theme/tokens/components/message";
import {CognitoUser, CognitoUserPool} from "amazon-cognito-identity-js";
import {ActivatedRoute, Router} from "@angular/router";
import {environment} from "../../../environment/environment";
import {FormsModule} from "@angular/forms";
import {MatInput} from "@angular/material/input";

@Component({
  selector: 'app-confirm-email',
  standalone: true,
  templateUrl: './confirm-email.component.html',
  imports: [
    MatFormField,
    MatButton,
    FormsModule,
    MatInput
  ],
  styleUrl: './confirm-email.component.css'
})
export class ConfirmEmailComponent implements OnInit {

  confirmationCode: string = '';
  username: string = 'popovicluka65@gmail.com';
  message: string = '';

  private userPoolData = {
    UserPoolId: environment.userPoolId, // Zameni sa svojim User Pool ID
    ClientId: environment.userPoolClientId // Zameni sa svojim Client ID
  };

  private userPool = new CognitoUserPool(this.userPoolData);


  constructor(private route: ActivatedRoute, private router: Router) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      console.log(params)
      this.username = "popovicluka65@gmail.com";
    });
  }

  confirmRegistration() {
    const userData = {
      Username: this.username,
      Pool: this.userPool
    };

    console.log(userData)
    const cognitoUser = new CognitoUser(userData);

    cognitoUser.confirmRegistration(this.confirmationCode, true, (err, result) => {

      console.log('Confirmation successful:', result);

      // Update email_verified attribute
      cognitoUser.getUserAttributes((errAttributes, attributes) => {
        if (errAttributes) {
          console.error('Error fetching user attributes:', errAttributes);
          this.message = 'Error fetching user attributes: ' + errAttributes.message;
          this.router.navigate(['/login']);
        }

        // @ts-ignore
        const attributeList = attributes.map(attribute => {
          return {
            Name: attribute.getName(),
            Value: attribute.getValue()
          };
        });

        attributeList.push({
          Name: 'email_verified',
          Value: 'true'
        });

        cognitoUser.updateAttributes(attributeList, (errUpdate, resultUpdate) => {
          if (errUpdate) {
            console.error('Failed to update attributes:', errUpdate);
            this.message = 'Failed to update attributes: ' + errUpdate.message;
            return;
          }

          console.log('Attributes updated successfully:', resultUpdate);
          this.message = 'Confirmation successful and attributes updated.';
          this.router.navigate(['/login']);
        });
      });
    });
  }

}
