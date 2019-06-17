import React from 'react';
import queryString from 'query-string';
import ApiAccountListAbsService from '../services/api-account-list-abs.service';

class AccountMenu extends React.Component {
    state = {};
    onLogoutClicked = e => {
        e.preventDefault();
        this.props.logout();
    };
    allAccount = async () => {
        const data = await ApiAccountListAbsService.call();

        this.props.history.push({
            pathname: '/account-page/all-account-page',
            search: queryString.stringify({
                jsonAllAccount: JSON.stringify(data['data']['data'])
            })
        });
    };




    render() {
        return (<nav>
  <ul>
    

        <li><a href="#" onClick={(e) => { e.preventDefault();
this.allAccount(); } }>All Account</a></li>

    

    

  </ul>
</nav>);
    }
}

export default AccountMenu;