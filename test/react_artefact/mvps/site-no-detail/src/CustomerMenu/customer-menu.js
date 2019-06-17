import React from 'react';
import { Link } from 'react-router-dom';
import queryString from 'query-string';
import ApiCustomerListAbsService from '../services/api-customer-list-abs.service';

class CustomerMenu extends React.Component {
  state = {};
  onLogoutClicked = e => {
    e.preventDefault();
    this.props.logout();
  };
  listCustomer = async () => {
    const data = await ApiCustomerListAbsService.call();

    this.props.history.push({
      pathname: '/customer-page/customer-content/list-customer-page',
      search: queryString.stringify({
        jsonAllCustomer: JSON.stringify(data['data']['data']),
      }),
    });
  };
  addCustomer = () => {
    this.props.history.push({
      pathname: '/customer-page/customer-content/add-customer-page',
    });
  };

  render() {
    return (
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>

          <li>
            <button
              onClick={e => {
                e.preventDefault();
                this.listCustomer();
              }}
            >
              List Customer
            </button>
          </li>
          <li>
            <button
              onClick={e => {
                e.preventDefault();
                this.addCustomer();
              }}
            >
              Add Customer
            </button>
          </li>
        </ul>
      </nav>
    );
  }
}

export default CustomerMenu;
