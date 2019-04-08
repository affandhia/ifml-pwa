import React from 'react';
import axios, { CancelToken } from 'axios';
import _debounce from 'lodash/debounce';

import Token from '../../utils/token';

import Form from '../../components/Form';

class CustomerPage extends React.Component {
  state = {
    source: CancelToken.source(),
    loading: false,
  };
  _isMounted = false;

  componentDidMount = () => {
    this._isMounted = true;
  };

  componentWillUnmount = () => {
    this._isMounted = false;

    this.state.source.cancel(
      'Operation canceled because of the component will be unmounted'
    );
  };

  addCustomer = _debounce(async (name, email, phone, address) => {
    const token = new Token().get();

    const encodedData = `name=${encodeURI(name)}&email=${encodeURI(
      email
    )}&phone=${encodeURI(phone)}&address=${encodeURI(address)}`;

    this.setState({
      loading: true,
    });

    try {
      const response = await axios.get(
        `/api/customer/create.abs?token=${token}&${encodedData}`,
        undefined,
        {
          cancelToken: this.state.source,
        }
      );

      if (this._isMounted) {
        this.setState({
          loading: false,
        });
      }
    } catch (e) {
      console.log(e);
      this.setState({
        loading: false,
      });
    }
  }, 1000);

  render() {
    if (this.state.loading) {
      return <div>Saving the data to database...</div>;
    }

    return (
      <Form
        formTitle="Add Customer"
        buttonText="Save Customer"
        onSubmit={this.addCustomer}
      />
    );
  }
}

export default CustomerPage;
