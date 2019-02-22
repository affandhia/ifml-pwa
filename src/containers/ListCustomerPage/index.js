import React from "react";
import axios, { CancelToken } from "axios";
import _debounce from "lodash/debounce";

class ListCustomerPage extends React.Component {
  state = {
    customers: [],
    source: CancelToken.source()
  };
  _isMounted = false;

  componentDidMount() {
    this._isMounted = true;

    this.getCustomerList();
  }

  componentWillUnmount() {
    this._isMounted = false;

    this.state.source.cancel(
      "Operation canceled because of the component will be unmounted"
    );
  }

  getCustomerList = _debounce(async (token = "") => {
    token = token ? token : localStorage.getItem("token");
    try {
      const response = await axios.get(
        `http://localhost:8089/api/customer/list.abs?token=${token}`,
        undefined,
        {
          cancelToken: this.state.source
        }
      );

      if (this._isMounted) {
        this.setState({
          customers: response.data.data
        });
      }
    } catch (e) {
      console.log(e);
    }
  }, 1000);

  handleTokenChange = e => {
    this.getCustomerList(e.target.value);
  };

  renderCustomerList = () => {
    const { customers } = this.state;

    return (
      <React.Fragment>
        {customers.map(customer => {
          const { email, id, name } = customer;

          return (
            <li key={id}>
              <div>Customer ID: {id}</div>
              <div>{name}</div>
              <div>{email}</div>
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
        <ul>{this.renderCustomerList()}</ul>
      </React.Fragment>
    );
  }
}

export default ListCustomerPage;
