import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'add-customer-page',
    templateUrl: './add-customer-page.component.html',
    styleUrls: ['./add-customer-page.component.css']
})
export class AddCustomerPageComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {});
    }



}