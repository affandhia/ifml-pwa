import React from 'react';
import './App.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { CookiesProvider } from 'react-cookie';

import { AuthProvider, AuthConsumer } from './containers/Authentication';

import AddCustomerPage from './containers/AddCustomerPage';
import ListCustomerPage from './containers/ListCustomerPage';
import DetailCustomerPage from './containers/DetailCustomerPage';
import LoginPage from './containers/LoginPage';
import ListAccountPage from './containers/ListAccountPage';

import Navbar from './components/Navbar';

const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const NotFound = () => (
  <div>
    <h2>404 Uh-Oh</h2>
  </div>
);

const App = () => (
  <CookiesProvider>
    <BrowserRouter>
      <AuthProvider>
        <div>
          <AuthConsumer>{values => <Navbar {...values} />}</AuthConsumer>

          <hr />

          <Switch>
            <Route exact path="/" component={Home} />
            <Route exact path="/login" component={LoginPage} />

            <Route exact path="/account" component={ListAccountPage} />
            <Route exact path="/customer" component={ListCustomerPage} />
            <Route exact path="/customer/add" component={AddCustomerPage} />
            <Route exact path="/customer/:id" component={DetailCustomerPage} />
            <Route component={NotFound}/>
          </Switch>

        </div>
      </AuthProvider>
    </BrowserRouter>
  </CookiesProvider>
);

export default App;
