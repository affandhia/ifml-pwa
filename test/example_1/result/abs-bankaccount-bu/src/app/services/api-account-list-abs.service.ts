import {
    Injectable
} from '@angular/core';
import {
    environment
} from '../../environments/environment';
import {
    HttpClient,
    HttpHeaders,
    HttpParams
} from '@angular/common/http';


@Injectable({
    providedIn: 'root'
})
export class ApiAccountListAbsService {



    constructor(private http: HttpClient) {

    }

    httpOptions = {

        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        })
    };

    endpoint: string = environment.rootApi + 'api/account/list.abs';

    call() {
        let httpParams = new HttpParams();

        let key_token = 'token';
        let googleToken = localStorage.getItem(key_token);
        httpParams = httpParams.append(key_token, googleToken);


        this.httpOptions['params'] = httpParams;
        return this.http.get(this.endpoint, this.httpOptions).toPromise();
    }
}