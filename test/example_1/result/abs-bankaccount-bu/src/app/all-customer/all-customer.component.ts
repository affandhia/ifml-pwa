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
import {
    ApiCustomerRetrieveAbsService
} from '../services/api-customer-retrieve-abs.service';
import {
    ApiCustomerDeleteAbsService
} from '../services/api-customer-delete-abs.service';

@Component({
    selector: 'all-customer',
    templateUrl: './all-customer.component.html',
    styleUrls: ['./all-customer.component.css']
})
export class AllCustomerComponent implements OnInit {

    @Input() jsonAllCustomer: any;
    public id: number;
    public allCustomerData: Customer;

    constructor(private route: ActivatedRoute, private router: Router, public apicustomerretrieveabsservice: ApiCustomerRetrieveAbsService, public apicustomerdeleteabsservice: ApiCustomerDeleteAbsService) {

    }

    ngOnInit() {
        this.attachallcustomerdata();
    }

    attachallcustomerdata() {
        this.allCustomerData = new Customer(this.jsonAllCustomer);
        this.id = this.allCustomerData.id;
    }
    details() {
        this.apicustomerretrieveabsservice.call({
            id: this.id
        }).then(data => {
            this.router.navigate(['/customer-page/customer-content/detail-customer-page'], {
                queryParams: {
                    objectDetailCustomer: JSON.stringify(data['data'])
                }
            });
        });
    }
    delete() {
        this.apicustomerdeleteabsservice.call({
            id: this.id
        }).then();
    }

}