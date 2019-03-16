import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'customer-page',
    templateUrl: './customer-page.component.html',
    styleUrls: ['./customer-page.component.css']
})
export class CustomerPageComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {

    }



}