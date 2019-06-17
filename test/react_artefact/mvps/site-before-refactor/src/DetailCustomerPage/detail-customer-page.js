import React from 'react';
import queryString from 'query-string';
import DetailCustomerComponent from '../DetailCustomer/detail-customer.js';

class DetailCustomerPage extends React.Component {
  state = {};
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
        {this.state.objectDetailCustomer !== undefined && (
          <DetailCustomerComponent
            {...this.props}
            objectDetailCustomer={this.state.objectDetailCustomer}
          />
        )}
      </React.Fragment>
    );
  }
}

export default DetailCustomerPage;
