import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'create-account-page',
    templateUrl: './create-account-page.component.html',
    styleUrls: ['./create-account-page.component.css']
})
export class CreateAccountPageComponent implements OnInit {

    public idOfTheAccountOwner: number;

    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {
            this.idOfTheAccountOwner = JSON.parse(params.idOfTheAccountOwner);
        });
    }



}