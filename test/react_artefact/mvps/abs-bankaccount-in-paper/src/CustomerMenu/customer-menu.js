import React from 'react';
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
                jsonAllCustomer: JSON.stringify(data['data']['data'])
            })
        });
    };
    addCustomer = () => {
        this.props.history.push({
            pathname: '/customer-page/customer-content/add-customer-page'

        });
    };




    render() {
        return (<nav>
  <ul>
    

        <li><a href="#" onClick={(e) => { e.preventDefault();
this.listCustomer(); } }>List Customer</a></li>
<li><a href="#" onClick={(e) => { e.preventDefault();
this.addCustomer(); } }>Add Customer</a></li>

    

    

  </ul>
</nav>);
    }
}

export default CustomerMenu;