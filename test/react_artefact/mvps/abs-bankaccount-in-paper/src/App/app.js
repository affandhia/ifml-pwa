import React from 'react';
import {
    AuthProvider,
    AuthConsumer,
    withAuth
} from '../Authentication';
import {
    BrowserRouter,
    Route,
    withRouter,
    Redirect,
    Switch
} from 'react-router-dom';
import {
    CookiesProvider
} from 'react-cookie';
import MainMenuComponent from '../MainMenu/main-menu.js';
import CustomerPageComponent from '../CustomerPage/customer-page.js';
import AccountPageComponent from '../AccountPage/account-page.js';
import LoginComponent from '../Login/login.js';

class App extends React.Component {
    state = {};




    render() {
        return (<CookiesProvider><BrowserRouter><AuthProvider>
<React.Fragment>
<AuthConsumer>{ (values) => {         const Component = withRouter(MainMenuComponent);
        return <Component {...values} />
         } }</AuthConsumer>
<Switch>
<Redirect exact from="" to={"/customer-page"}/>
<Route
  
  path="/customer-page"
  component={
  withAuth(CustomerPageComponent
  )

  }
/>
<Route
  
  path="/account-page"
  component={
  withAuth(AccountPageComponent
  )

  }
/>
<Route
  exact
  path="/login"
  component={LoginComponent

  }
/>
</Switch>
</React.Fragment>
</AuthProvider></BrowserRouter></CookiesProvider>);
    }
}

export default App;