import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';
import {
    ApiCustomerCreateAbsService
} from '../services/api-customer-create-abs.service';

@Component({
    selector: 'form-add-customer',
    templateUrl: './form-add-customer.component.html',
    styleUrls: ['./form-add-customer.component.css']
})
export class FormAddCustomerComponent implements OnInit {

    public customerName: string;
    public customerPhone: string;
    public customerEmail: string;
    public customerAddress: string;

    constructor(private route: ActivatedRoute, private router: Router, public apicustomercreateabsservice: ApiCustomerCreateAbsService) {

    }

    ngOnInit() {

    }

    save() {
        this.apicustomercreateabsservice.call({
            name: this.customerName,
            email: this.customerEmail,
            phone: this.customerPhone,
            address: this.customerAddress
        }).then(data => {
            this.router.navigate(['/customer-page/customer-content/list-customer-page'], {
                queryParams: {
                    jsonAllCustomer: JSON.stringify(data['data'])
                }
            });
        });
    }

}