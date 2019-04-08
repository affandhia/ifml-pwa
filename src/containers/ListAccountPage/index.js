import React from 'react';
import axios, { CancelToken } from 'axios';

import { withAuth } from '../Authentication';

import Token from '../../utils/token';

class ListAccountPage extends React.Component {
  state = {
    list: [],
    loading: null,
    source: CancelToken.source(),
  };
  _isMounted = false;

  componentDidMount() {
    this._isMounted = true;

    this.getList();
  }

  componentWillUnmount() {
    this._isMounted = false;

    this.state.source.cancel(
      'Operation canceled because of the component will be unmounted'
    );
  }

  getList = async (token = '') => {
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
          list: response.data.data,
        });
      }
    } catch (e) {
      console.log(e);
    }
  };

  renderList = () => {
    const { list } = this.state;

    return (
      <React.Fragment>
        {list.map(data => {
          const { rekening, balance, id, customerId, interest } = data;

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
        <ul>{this.renderList()}</ul>
      </React.Fragment>
    );
  }
}

export default withAuth(ListAccountPage);
