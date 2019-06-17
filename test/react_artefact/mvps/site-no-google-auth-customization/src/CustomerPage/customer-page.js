import React from 'react';
import { AuthConsumer, withAuth } from '../containers/Authentication';
import { withRouter, Redirect, Route, Switch } from 'react-router-dom';
import CustomerMenuComponent from '../CustomerMenu/customer-menu.js';
import CustomerContentComponent from '../CustomerContent/customer-content.js';

class CustomerPage extends React.Component {
  state = {};

  render() {
    return (
      <React.Fragment>
        <AuthConsumer>
          {values => {
            const Component = withRouter(CustomerMenuComponent);
            return <Component {...values} />;
          }}
        </AuthConsumer>
        <Switch>
          <Redirect
            exact
            from="/customer-page"
            to={'/customer-page/customer-content' + this.props.location.search}
          />
          <Route
            path="/customer-page/customer-content"
            component={withAuth(CustomerContentComponent)}
          />
        </Switch>
      </React.Fragment>
    );
  }
}

export default CustomerPage;
