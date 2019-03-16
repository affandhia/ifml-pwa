import {
    BrowserModule
} from '@angular/platform-browser';
import {
    NgModule
} from '@angular/core';
import {
    AppRoutingModule
} from './app-routing.module';
import {
    AppComponent
} from './app.component';
import {
    ServiceWorkerModule
} from '@angular/service-worker';
import {
    environment
} from '../environments/environment';
import {
    HttpClientModule
} from '@angular/common/http';
import {
    FormsModule
} from '@angular/forms';
import {
    NgxSmartModalModule,
    NgxSmartModalService
} from 'ngx-smart-modal';
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
    GoogleLoginProvider,
    AuthServiceConfig,
    SocialLoginModule
} from 'angular-6-social-login-v2';


export function getAuthServiceConfigs() {
    let config = new AuthServiceConfig(
        [{
            id: GoogleLoginProvider.PROVIDER_ID,
            provider: new GoogleLoginProvider("980984936575-0lo321pevqjlul7nsdk441ccjah11b1f.apps.googleusercontent.com")
        }]
    );
    return config;
}


@NgModule({
    declarations: [
        AppComponent,
        MainMenuComponent,
        CustomerMenuComponent,
        FormAddCustomerComponent,
        AddCustomerPageComponent,
        AllCustomerComponent,
        ListCustomerPageComponent,
        DetailCustomerComponent,
        DetailCustomerPageComponent,
        NewAccountFormComponent,
        CreateAccountPageComponent,
        CustomerContentComponent,
        CustomerPageComponent,
        AccountMenuComponent,
        AllAccountComponent,
        AllAccountPageComponent,
        AccountPageComponent,
        LoginComponent,
        LoginComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        NgxSmartModalModule.forRoot(),
        AppRoutingModule,
        FormsModule,
        ServiceWorkerModule.register('/abs-bankaccount/ngsw-worker.js', {
            enabled: environment.production
        }),
        SocialLoginModule
    ],
    providers: [NgxSmartModalService, {
        provide: AuthServiceConfig,
        useFactory: getAuthServiceConfigs
    }],
    bootstrap: [AppComponent]
})
export class AppModule {}