import React from 'react';
import queryString from 'query-string';

class DetailCustomer extends React.Component {
  state = {};
  componentWillMount = () => {
    this.customerData = this.props.objectDetailCustomer;
    this.idCust = this.customerData.id;
  };
  createNewAccount = () => {
    this.props.history.push({
      pathname: '/customer-page/customer-content/create-account-page',
      search: queryString.stringify({
        idOfTheAccountOwner: JSON.stringify(this.idCust),
      }),
    });
  };

  render() {
    return (
      <React.Fragment>
        <div>
          <strong>Name</strong>
          <div>{this.customerData && this.customerData.name}</div>
          <br />
        </div>
        <div>
          <strong>Email</strong>
          <div>{this.customerData && this.customerData.email}</div>
          <br />
        </div>
        <div>
          <strong>Phone Number</strong>
          <div>{this.customerData && this.customerData.phone}</div>
          <br />
        </div>
        <div>
          <strong>Address</strong>
          <div>{this.customerData && this.customerData.address}</div>
          <br />
        </div>
        <div>
          <label htmlFor="input-id-cust">
            <strong>Id Cust</strong>
          </label>
          <div>
            <input
              id="input-id-cust"
              name="idCustInput"
              type="number"
              placeholder="Fill the Id Cust"
              defaultValue={this.customerData.idCust}
              ref={e => {
                this.idCustInput = e;
              }}
            />
          </div>
          <br />
        </div>
        <button
          onClick={e => {
            e.preventDefault();
            this.createNewAccount();
          }}
        >
          Create New Account
        </button>
      </React.Fragment>
    );
  }
}

export default DetailCustomer;
