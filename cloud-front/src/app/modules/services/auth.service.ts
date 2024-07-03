import { Injectable } from '@angular/core';
import {AuthenticationDetails, CognitoUser, CognitoUserPool, CognitoUserSession} from "amazon-cognito-identity-js";
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

  getEmail():string{
    try {
      const storedUser = localStorage.getItem('currentUser');
      if (storedUser) {
        const token = this.decodeJwtToken(storedUser);
        return token['email']
      }
      return "";
    } catch (error) {
      console.error('Error fetching user email:', error);
      return "";
    }
  }

  //potencijalno napraviti i getUsernameStorage
  getRole():string| null {
    try {
      const storedUser = localStorage.getItem('currentUser');
      if (storedUser) {
        const groups = this.decodeJwtToken(storedUser);
         if (groups && groups['cognito:groups']) {
          for (let group of groups['cognito:groups']) {
            if (group === 'admin') {
              return 'admin';
            }
            if (group === 'user') {
              return 'user';
            }
        }
        }
      }
      return null;
    } catch (error) {
      console.error('Error fetching user role:', error);
      return null;
    }
  }
  private decodeJwtToken(idToken: string): any | null {
    try {
      const tokenParts = idToken.split('.');
      const payload = JSON.parse(atob(tokenParts[1]));
      return payload;
    } catch (error) {
      console.error('Error decoding JWT token:', error);
      return null;
    }
  }
}
