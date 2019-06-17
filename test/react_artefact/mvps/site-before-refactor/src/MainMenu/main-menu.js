import React from 'react';
import { Link } from 'react-router-dom';

class MainMenu extends React.Component {
  state = {};
  onLogoutClicked = e => {
    e.preventDefault();
    this.props.logout();
  };
  customer = () => {
    this.props.history.push({
      pathname: '/customer-page',
    });
  };
  account = () => {
    this.props.history.push({
      pathname: '/account-page',
    });
  };

  render() {
    return (
      <nav>
        <ul>
          {this.props.isAuth ? (
            <React.Fragment>
              <li>
                <a
                  href="#"
                  onClick={e => {
                    e.preventDefault();
                    this.customer();
                  }}
                >
                  Customer
                </a>
              </li>
              <li>
                <a
                  href="#"
                  onClick={e => {
                    e.preventDefault();
                    this.account();
                  }}
                >
                  Account
                </a>
              </li>
            </React.Fragment>
          ) : null}

          {this.props.isAuth ? (
            <li>
              <a href="/" onClick={this.onLogoutClicked}>
                Logout
              </a>
            </li>
          ) : (
            <li>
              <Link to="/login">Login</Link>
            </li>
          )}
        </ul>
      </nav>
    );
  }
}

export default MainMenu;
