import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';
import AddCustomerPageComponent from '../AddCustomerPage/add-customer-page.js';
import { withAuth } from '../containers/Authentication';
import ListCustomerPageComponent from '../ListCustomerPage/list-customer-page.js';
import DetailCustomerPageComponent from '../DetailCustomerPage/detail-customer-page.js';
import CreateAccountPageComponent from '../CreateAccountPage/create-account-page.js';

class CustomerContent extends React.Component {
  state = {};

  render() {
    return (
      <React.Fragment>
        <Switch>
          <Redirect
            exact
            from="/customer-page/customer-content"
            to={
              '/customer-page/customer-content/add-customer-page' +
              this.props.location.search
            }
          />
          <Route
            exact
            path="/customer-page/customer-content/add-customer-page"
            component={withAuth(AddCustomerPageComponent)}
          />
          <Route
            exact
            path="/customer-page/customer-content/list-customer-page"
            component={withAuth(ListCustomerPageComponent)}
          />
          <Route
            exact
            path="/customer-page/customer-content/detail-customer-page"
            component={withAuth(DetailCustomerPageComponent)}
          />
          <Route
            exact
            path="/customer-page/customer-content/create-account-page"
            component={withAuth(CreateAccountPageComponent)}
          />
        </Switch>
      </React.Fragment>
    );
  }
}

export default CustomerContent;
