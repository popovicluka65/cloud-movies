import { Injectable } from '@angular/core';
import {CognitoUser, CognitoUserPool} from "amazon-cognito-identity-js";
import {environment} from "../../environment/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userPool: CognitoUserPool;
  constructor() {
    this.userPool = new CognitoUserPool({
      UserPoolId: environment.userPoolId,
      ClientId: environment.userPoolClientId
    });
  }

  getCurrentUser(): CognitoUser | null {
    return this.userPool.getCurrentUser();
  }

  getUsername(): string | null {
    const currentUser = this.getCurrentUser();
    if (currentUser) {
      return currentUser.getUsername();
    }
    return null;
  }
}
