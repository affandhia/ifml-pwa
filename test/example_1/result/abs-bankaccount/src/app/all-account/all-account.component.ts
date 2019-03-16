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

@Component({
    selector: 'all-account',
    templateUrl: './all-account.component.html',
    styleUrls: ['./all-account.component.css']
})
export class AllAccountComponent implements OnInit {

    @Input() jsonAllAccount: any;
    public allAccountData: Account;

    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.attachallaccountdata();
    }

    attachallaccountdata() {
        this.allAccountData = new Account(this.jsonAllAccount);
    }
    seedetail() {

    }

}