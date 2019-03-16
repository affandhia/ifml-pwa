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
    Account
} from '../models/account.model';
import {
    ApiAccountCreateAbsService
} from '../services/api-account-create-abs.service';

@Component({
    selector: 'new-account-form',
    templateUrl: './new-account-form.component.html',
    styleUrls: ['./new-account-form.component.css']
})
export class NewAccountFormComponent implements OnInit {

    public existingCustomer: Account;
    @Input() idOfTheAccountOwner: number;
    public theAccount: string;
    public balance: number;

    constructor(private route: ActivatedRoute, private router: Router, public apiaccountcreateabsservice: ApiAccountCreateAbsService) {

    }

    ngOnInit() {
        this.attachexistingcustomer();
    }

    attachexistingcustomer() {
        this.existingCustomer = new Account({
            customerId: this.idOfTheAccountOwner
        });
    }
    submit() {
        this.apiaccountcreateabsservice.call({
            customerId: this.idOfTheAccountOwner,
            rekening: this.theAccount,
            balance: this.balance
        }).then();
    }

}