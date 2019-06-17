import React from 'react';
import queryString from 'query-string';
import AllCustomerComponent from '../AllCustomer/all-customer.js';

class ListCustomerPage extends React.Component {
  state = {};
  componentDidMount = () => {
    this.setState({
      jsonAllCustomer: JSON.parse(
        queryString.parse(this.props.location.search).jsonAllCustomer
      ),
    });
  };

  render() {
    return (
      <React.Fragment>
        <ul
          id="list-AllCustomerComponent"
          className="list-component view-component"
        >
          {this.state.jsonAllCustomer &&
            this.state.jsonAllCustomer.map(jsonAllCustomer => (
              <AllCustomerComponent
                {...this.props}
                jsonAllCustomer={jsonAllCustomer}
              />
            ))}
        </ul>
      </React.Fragment>
    );
  }
}

export default ListCustomerPage;
