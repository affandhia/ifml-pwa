import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';
import {
    ApiCustomerListAbsService
} from '../services/api-customer-list-abs.service';

@Component({
    selector: 'customer-menu',
    templateUrl: './customer-menu.component.html',
    styleUrls: ['./customer-menu.component.css']
})
export class CustomerMenuComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router, public apicustomerlistabsservice: ApiCustomerListAbsService) {

    }

    ngOnInit() {

    }

    listcustomer() {
        this.apicustomerlistabsservice.call().then(data => {
            this.router.navigate(['/customer-page/customer-content/list-customer-page'], {
                queryParams: {
                    jsonAllCustomer: JSON.stringify(data['data'])
                }
            });
        });
    }
    addcustomer() {
        this.router.navigate(['/customer-page/customer-content/add-customer-page']);
    }

}