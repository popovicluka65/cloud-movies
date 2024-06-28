import { Injectable } from '@angular/core';
import {AuthUser,getCurrentUser,signOut,fetchAuthSession,AuthTokens} from "aws-amplify/auth";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }

  async getCurrentUser(): Promise<AuthUser>{
    return await getCurrentUser();
  }

  async getCurrentSession(): Promise<AuthTokens | undefined>{
    return (await fetchAuthSession()).tokens;
  }

  async getCurrentUserFullname(): Promise<string|undefined>{
    let cognito = await (await fetchAuthSession()).tokens;
    return cognito?.idToken?.payload['name']?.toString();
  }

  signOut(){
    signOut();
  }
}
