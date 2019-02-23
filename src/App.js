import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom'

import CustomerPage from './containers/CustomerPage';
import ListAccountPage from './containers/ListAccountPage';

import Navbar from './components/Navbar';

const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
)

const App = () => (
  <Router>
    <div>
      <Navbar />

      <hr/>

      <Route exact path="/" component={Home}/>
      <Route path="/customer" component={CustomerPage}/>
      <Route path="/account" component={ListAccountPage}/>
    </div>
  </Router>
)

export default App;
