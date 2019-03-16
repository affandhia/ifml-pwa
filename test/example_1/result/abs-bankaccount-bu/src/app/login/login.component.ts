import {
    Component,
    OnInit
} from '@angular/core';
import {
    AuthService,
    GoogleLoginProvider
} from 'angular-6-social-login-v2';

@Component({
    selector: 'login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

    constructor(private socialAuthService: AuthService) {}

    public isLoggedIn = false;
    public profileImage = "";

    ngOnInit() {
        if (localStorage.getItem('token')) {
            this.isLoggedIn = true;
            this.profileImage = localStorage.getItem('image');
        } else {
            this.isLoggedIn = false;
        }
    }

    public socialSignIn() {
        let socialPlatformProvider = GoogleLoginProvider.PROVIDER_ID;
        this.socialAuthService.signIn(socialPlatformProvider).then(
            (data) => {
                let userData = data;
                localStorage.setItem('token', data['idToken']);
                localStorage.setItem('image', data['image']);
                location.reload();
            }
        );
    }

    public logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('image');
        location.reload();
    }

}