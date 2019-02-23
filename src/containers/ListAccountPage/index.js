import React from "react";
import axios, { CancelToken } from "axios";
import _debounce from "lodash/debounce";

import Token from "../../utils/token";

class ListAccountPage extends React.Component {
  state = {
    accounts: [],
    loading: null,
    source: CancelToken.source()
  };
  _isMounted = false;

  componentDidMount() {
    this._isMounted = true;

    this.getAccountList();
  }

  componentWillUnmount() {
    this._isMounted = false;

    this.state.source.cancel(
      "Operation canceled because of the component will be unmounted"
    );
  }

  getAccountList = async (token = '') => {
    token = token ? token : new Token().get();

    try {
      const response = await axios.get(
        `http://localhost:8089/api/account/list.abs?token=${token}`,
        undefined,
        {
          cancelToken: this.state.source
        }
      );

      if (this._isMounted) {
        this.setState({
          accounts: response.data.data
        });
      }
    } catch (e) {
      console.log(e);
    }
  };

  getAccountListDebounced = _debounce(this.getAccountList, 1000);

  handleTokenChange = e => {
    this.getAccountListDebounced(e.target.value);
  };

  renderAccountList = () => {
    const { accounts } = this.state;

    return (
      <React.Fragment>
        {accounts.map(account => {
          const { rekening, balance, id, accountId, interest } = account;

          return (
            <li key={id}>
              <div>Account ID: {id}</div>
              <div>Customer ID: {accountId}</div>
              <div>{rekening}</div>
              <div>{interest}</div>
              <div>{balance}</div>
            </li>
          );
        })}
      </React.Fragment>
    );
  };

  render() {
    return (
      <React.Fragment>
        <div>Input the Token here</div>
        <div>
          <textarea onChange={this.handleTokenChange} />
        </div>
        {this.state.loading ? <div>{this.state.loading}</div> : null}
        <ul>{this.renderAccountList()}</ul>
      </React.Fragment>
    );
  }
}

export default ListAccountPage;
