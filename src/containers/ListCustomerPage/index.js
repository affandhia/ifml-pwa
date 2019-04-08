import React from 'react';
import axios, { CancelToken } from 'axios';
import { Link } from 'react-router-dom';
import _debounce from 'lodash/debounce';

import Token from '../../utils/token';

class ListCustomerPage extends React.Component {
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
        `/api/customer/list.abs?token=${token}`,
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

  deleteCustomerList = _debounce(async id => {
    const token = new Token().get();

    this.setState({
      loading: `Deleting customer ${id}`,
    });

    try {
      await axios.get(
        `/api/customer/delete.abs?token=${token}&id=${id}`,
        undefined,
        {
          cancelToken: this.state.source,
        }
      );

      if (this._isMounted) {
        this.setState({
          loading: null,
        });

        this.getList();
      }
    } catch (e) {
      console.log(e);
      this.setState({
        loading: null,
      });
    }
  }, 1000);

  handleDeleteCustomer = id => () => {
    this.deleteCustomerList(id);
  };

  renderList = () => {
    const { list } = this.state;

    return (
      <React.Fragment>
        {list.map(data => {
          const { email, id, name } = data;

          return (
            <li key={id}>
              <div>Customer ID: {id.toString()}</div>
              <div>{name}</div>
              <div>{email}</div>
              <div>
                <Link to={`/customer/${id}`}>
                  <button>Details</button>
                </Link>
                <button onClick={this.handleDeleteCustomer(id)}>Delete</button>
              </div>
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

export default ListCustomerPage;
