import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { CookiesProvider } from 'react-cookie';

import { AuthProvider, AuthConsumer } from './containers/Authentication';

import CustomerPage from './containers/CustomerPage';
import LoginPage from './containers/LoginPage';
import ListAccountPage from './containers/ListAccountPage';

import Navbar from './components/Navbar';

const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const App = () => (
  <CookiesProvider>
    <Router>
      <AuthProvider>
        <div>
          <AuthConsumer>{values => <Navbar {...values} />}</AuthConsumer>

          <hr />

          <Route exact path="/" component={Home} />
          <Route exact path="/login" component={LoginPage} />
          <Route path="/customer" component={CustomerPage} />
          <Route path="/account" component={ListAccountPage} />
        </div>
      </AuthProvider>
    </Router>
  </CookiesProvider>
);

export default App;
