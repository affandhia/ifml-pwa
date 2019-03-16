import {
    NgModule
} from '@angular/core';
import {
    Routes,
    RouterModule
} from '@angular/router';
import {
    MainMenuComponent
} from './main-menu/main-menu.component';
import {
    CustomerMenuComponent
} from './customer-menu/customer-menu.component';
import {
    FormAddCustomerComponent
} from './form-add-customer/form-add-customer.component';
import {
    AddCustomerPageComponent
} from './add-customer-page/add-customer-page.component';
import {
    AllCustomerComponent
} from './all-customer/all-customer.component';
import {
    ListCustomerPageComponent
} from './list-customer-page/list-customer-page.component';
import {
    DetailCustomerComponent
} from './detail-customer/detail-customer.component';
import {
    DetailCustomerPageComponent
} from './detail-customer-page/detail-customer-page.component';
import {
    NewAccountFormComponent
} from './new-account-form/new-account-form.component';
import {
    CreateAccountPageComponent
} from './create-account-page/create-account-page.component';
import {
    CustomerContentComponent
} from './customer-content/customer-content.component';
import {
    CustomerPageComponent
} from './customer-page/customer-page.component';
import {
    AccountMenuComponent
} from './account-menu/account-menu.component';
import {
    AllAccountComponent
} from './all-account/all-account.component';
import {
    AllAccountPageComponent
} from './all-account-page/all-account-page.component';
import {
    AccountPageComponent
} from './account-page/account-page.component';
import {
    LoginComponent
} from './login/login.component';
import {
    AuthGuard
} from './guard/auth.guard';

const routes: Routes = [{
    path: '',
    redirectTo: 'customer-page',
    pathMatch: 'full'
}, {
    path: 'customer-page',
    component: CustomerPageComponent,
    canActivate: [AuthGuard],
    children: [{
        path: '',
        redirectTo: 'customer-content',
        pathMatch: 'full'
    }, {
        path: 'customer-content',
        component: CustomerContentComponent,
        canActivate: [AuthGuard],
        children: [{
            path: '',
            redirectTo: 'add-customer-page',
            pathMatch: 'full'
        }, {
            path: 'add-customer-page',
            component: AddCustomerPageComponent,
            canActivate: [AuthGuard]
        }, {
            path: 'list-customer-page',
            component: ListCustomerPageComponent,
            canActivate: [AuthGuard]
        }, {
            path: 'detail-customer-page',
            component: DetailCustomerPageComponent,
            canActivate: [AuthGuard]
        }, {
            path: 'create-account-page',
            component: CreateAccountPageComponent,
            canActivate: [AuthGuard]
        }]
    }]
}, {
    path: 'account-page',
    component: AccountPageComponent,
    canActivate: [AuthGuard],
    children: [{
        path: 'all-account-page',
        component: AllAccountPageComponent,
        canActivate: [AuthGuard]
    }]
}, {
    path: 'login',
    component: LoginComponent
}];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}