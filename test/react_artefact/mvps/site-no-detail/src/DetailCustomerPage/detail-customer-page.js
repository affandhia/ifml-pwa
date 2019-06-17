import React from 'react';
import queryString from 'query-string';
import DetailCustomerComponent from '../DetailCustomer/detail-customer.js';

class DetailCustomerPage extends React.Component {
  state = {};
  objectDetailCustomer;
  componentDidMount = () => {
    this.setState({
      objectDetailCustomer: JSON.parse(
        queryString.parse(this.props.location.search).objectDetailCustomer
      ),
    });
  };

  render() {
    return (
      <React.Fragment>
        <DetailCustomerComponent
          {...this.props}
          objectDetailCustomer={this.state.objectDetailCustomer || {}}
        />
      </React.Fragment>
    );
  }
}

export default DetailCustomerPage;
