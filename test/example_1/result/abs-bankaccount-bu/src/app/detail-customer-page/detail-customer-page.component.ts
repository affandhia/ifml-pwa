import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';
import {
    Customer
} from '../models/customer.model';

@Component({
    selector: 'detail-customer-page',
    templateUrl: './detail-customer-page.component.html',
    styleUrls: ['./detail-customer-page.component.css']
})
export class DetailCustomerPageComponent implements OnInit {

    public objectDetailCustomer: Customer;

    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {
            this.objectDetailCustomer = new Customer(JSON.parse(params.objectDetailCustomer));
        });
    }



}