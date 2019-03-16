import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'customer-content',
    templateUrl: './customer-content.component.html',
    styleUrls: ['./customer-content.component.css']
})
export class CustomerContentComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {

    }



}