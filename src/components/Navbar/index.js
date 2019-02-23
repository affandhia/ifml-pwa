import React, { useCallback } from 'react';
import { Link } from 'react-router-dom';

class Navbar extends React.Component {
  onLogoutClicked = e => {
    e.preventDefault();
    this.props.logout();
  };

  renderMenu = () => {
    if (!this.props.isAuth) return null;

    return (
      <React.Fragment>
        <li>
          <Link to="/customer">Customer</Link>
        </li>
        <li>
          <Link to="/account">Account</Link>
        </li>
      </React.Fragment>
    );
  };

  renderAuthMenu = () => {
    if (this.props.isAuth) {
      return (
        <li>
          <a href="/" onClick={this.onLogoutClicked}>
            Logout
          </a>
        </li>
      );
    }

    return (
      <li>
        <Link to="/login">Login</Link>
      </li>
    );
  };

  render() {
    return (
      <ul>
        {this.renderMenu()}
        {this.renderAuthMenu()}
      </ul>
    );
  }
}

export default Navbar;
