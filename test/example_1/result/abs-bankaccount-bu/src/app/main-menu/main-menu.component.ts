import {
    Component,
    OnInit
} from '@angular/core';
import {
    ActivatedRoute,
    Router
} from '@angular/router';

@Component({
    selector: 'main-menu',
    templateUrl: './main-menu.component.html',
    styleUrls: ['./main-menu.component.css']
})
export class MainMenuComponent implements OnInit {



    constructor(private route: ActivatedRoute, private router: Router) {

    }

    ngOnInit() {

    }

    customer() {
        this.router.navigate(['/customer-page']);
    }
    account() {
        this.router.navigate(['/account-page']);
    }

}