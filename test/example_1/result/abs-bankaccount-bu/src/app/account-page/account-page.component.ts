import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'account-page',
    templateUrl: './account-page.component.html',
    styleUrls: ['./account-page.component.css']
})
export class AccountPageComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {

    }



}