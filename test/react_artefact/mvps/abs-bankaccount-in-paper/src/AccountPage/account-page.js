import React from 'react';
import {
    AuthConsumer,
    withAuth
} from '../Authentication';
import {
    withRouter,
    Route,
    Switch
} from 'react-router-dom';
import AccountMenuComponent from '../AccountMenu/account-menu.js';
import AllAccountPageComponent from '../AllAccountPage/all-account-page.js';

class AccountPage extends React.Component {
    state = {};




    render() {
        return (<React.Fragment>
<AuthConsumer>{ (values) => {         const Component = withRouter(AccountMenuComponent);
        return <Component {...values} />
         } }</AuthConsumer>
<Switch>
<Route
  exact
  path="/account-page/all-account-page"
  component={
  withAuth(AllAccountPageComponent
  )

  }
/>
</Switch>
</React.Fragment>);
    }
}

export default AccountPage;