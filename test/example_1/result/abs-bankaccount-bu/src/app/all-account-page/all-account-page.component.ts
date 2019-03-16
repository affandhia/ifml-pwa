import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'all-account-page',
    templateUrl: './all-account-page.component.html',
    styleUrls: ['./all-account-page.component.css']
})
export class AllAccountPageComponent implements OnInit {

    public jsonAllAccount: any;

    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {
            this.jsonAllAccount = JSON.parse(params.jsonAllAccount);
        });
    }



}