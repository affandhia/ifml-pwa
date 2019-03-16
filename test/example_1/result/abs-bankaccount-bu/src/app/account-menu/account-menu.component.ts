import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';
import {
    ApiAccountListAbsService
} from '../services/api-account-list-abs.service';

@Component({
    selector: 'account-menu',
    templateUrl: './account-menu.component.html',
    styleUrls: ['./account-menu.component.css']
})
export class AccountMenuComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router, public apiaccountlistabsservice: ApiAccountListAbsService) {

    }

    ngOnInit() {

    }

    allaccount() {
        this.apiaccountlistabsservice.call().then(data => {
            this.router.navigate(['/account-page/all-account-page'], {
                queryParams: {
                    jsonAllAccount: JSON.stringify(data['data'])
                }
            });
        });
    }

}