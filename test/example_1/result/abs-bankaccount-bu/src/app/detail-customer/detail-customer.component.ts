import {
    Component,
    OnInit,
    Input
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';
import {
    Customer
} from '../models/customer.model';

@Component({
    selector: 'detail-customer',
    templateUrl: './detail-customer.component.html',
    styleUrls: ['./detail-customer.component.css']
})
export class DetailCustomerComponent implements OnInit {

    @Input() objectDetailCustomer: Customer;
    public idCust: number;
    public customerData: Customer;

    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.attachcustomerdata();
    }

    attachcustomerdata() {
        this.customerData = this.objectDetailCustomer;
        this.idCust = this.customerData.id;
    }
    createnewaccount() {
        this.router.navigate(['/customer-page/customer-content/create-account-page'], {
            queryParams: {
                idOfTheAccountOwner: JSON.stringify(this.idCust)
            }
        });
    }

}