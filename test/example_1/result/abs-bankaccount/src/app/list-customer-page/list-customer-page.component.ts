import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'list-customer-page',
    templateUrl: './list-customer-page.component.html',
    styleUrls: ['./list-customer-page.component.css']
})
export class ListCustomerPageComponent implements OnInit {

    public jsonAllCustomer: any;

    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {
            this.jsonAllCustomer = JSON.parse(params.jsonAllCustomer);
        });
    }



}