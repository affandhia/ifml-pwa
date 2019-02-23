import React from "react";
import { Switch, Route, Redirect } from "react-router-dom";

import AddCustomerPage from "../AddCustomerPage";
import ListCustomerPage from "../ListCustomerPage";
import DetailCustomerPage from "../DetailCustomerPage";

import Navbar from "./components/Navbar";

class CustomerPage extends React.Component {
  render() {
    const { match } = this.props;

    return (
      <React.Fragment>
        <Navbar match={match}/>
        <hr />
        <Switch>
          <Route exact path={`${match.url}/add`} component={AddCustomerPage} />
        <Route exact path={`${match.url}/:id`} component={DetailCustomerPage} />
          <Route exact path={`${match.url}/`} component={ListCustomerPage} />
          <Redirect
            from={`${match.url}/`}
            to={match.url}
          />
        </Switch>
      </React.Fragment>
    );
  }
}

export default CustomerPage;
