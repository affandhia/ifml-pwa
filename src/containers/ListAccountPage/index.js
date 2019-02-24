import React from 'react';
import axios, { CancelToken } from 'axios';

import { withAuth } from '../Authentication';

import Token from '../../utils/token';

class ListAccountPage extends React.Component {
  state = {
    accounts: [],
    loading: null,
    source: CancelToken.source(),
  };
  _isMounted = false;

  componentDidMount() {
    this._isMounted = true;

    this.getAccountList();
  }

  componentWillUnmount() {
    this._isMounted = false;

    this.state.source.cancel(
      'Operation canceled because of the component will be unmounted'
    );
  }

  getAccountList = async (token = '') => {
    token = token ? token : new Token().get();

    try {
      const response = await axios.get(
        `/api/account/list.abs?token=${token}`,
        undefined,
        {
          cancelToken: this.state.source,
        }
      );

      if (this._isMounted) {
        this.setState({
          accounts: response.data.data,
        });
      }
    } catch (e) {
      console.log(e);
    }
  };

  renderAccountList = () => {
    const { accounts } = this.state;

    return (
      <React.Fragment>
        {accounts.map(account => {
          const { rekening, balance, id, customerId, interest } = account;

          return (
            <li key={id}>
              <div>Account ID: {id}</div>
              <div>Customer ID: {customerId}</div>
              <div>Bank Account: {rekening}</div>
              <div>Interest: {interest}</div>
              <div>Balance: {balance}</div>
            </li>
          );
        })}
      </React.Fragment>
    );
  };

  render() {
    return (
      <React.Fragment>
        {this.state.loading ? <div>{this.state.loading}</div> : null}
        <ul>{this.renderAccountList()}</ul>
      </React.Fragment>
    );
  }
}

export default withAuth(ListAccountPage);
