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
export class ApiCustomerDeleteAbsService {



    constructor(private http: HttpClient) {

    }

    httpOptions = {

        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        })
    };

    endpoint: string = environment.rootApi + 'api/customer/delete.abs';

    call(param) {
        let httpParams = new HttpParams();

        let key_token = 'token';
        let googleToken = localStorage.getItem(key_token);
        httpParams = httpParams.append(key_token, googleToken);


        Object.keys(param).forEach(function(key) {
            httpParams = httpParams.append(key, param[key]);
        });

        this.httpOptions['params'] = httpParams;
        return this.http.get(this.endpoint, this.httpOptions).toPromise();
    }
}