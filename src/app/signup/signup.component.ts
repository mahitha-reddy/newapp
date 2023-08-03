import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observer } from 'rxjs';


interface UserData {
  username: string;
  email: string;
  password: string;
}
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  userData: UserData = {
    username: '',
    email: '',
    password: ''
  };
  message: string | null = null;

  constructor(private http: HttpClient) { }

  signup(): void {
    this.http.post<any>('http://localhost:5000/signup', this.userData).subscribe({
      next: (response) => {
        this.message = 'Signup successful!';
      },
      error: (error) => {
        this.message = error.error.message || 'An error occurred. Please try again later.';
      }
    });
  }


}
