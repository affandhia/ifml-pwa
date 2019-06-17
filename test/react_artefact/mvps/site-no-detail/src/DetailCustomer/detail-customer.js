import React from 'react';
import queryString from 'query-string';

class DetailCustomer extends React.Component {
  state = {};
  customerData = this.state.objectDetailCustomer || {};
  idCust = this.customerData.id;
  componentDidMount() {
    this.customerData = this.props.objectDetailCustomer || {};
  }
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
        <React.Fragment>
          <div
            id="div-vis-name"
            className="view-component-part visualization-attribute"
          >
            <p id="label-vis-name" className="label-visualization">
              Name
            </p>
            <p id="vs-name" className="class-attribute">
              {this.customerData && this.customerData.name}
            </p>
          </div>
          <div
            id="div-vis-email"
            className="view-component-part visualization-attribute"
          >
            <p id="label-vis-email" className="label-visualization">
              Email
            </p>
            <p id="vs-email" className="class-attribute">
              {this.customerData && this.customerData.email}
            </p>
          </div>
          <div
            id="div-vis-phone-number"
            className="view-component-part visualization-attribute"
          >
            <p id="label-vis-phone-number" className="label-visualization">
              Phone Number
            </p>
            <p id="vs-phone-number" className="class-attribute">
              {this.customerData && this.customerData.phone}
            </p>
          </div>
          <div
            id="div-vis-address"
            className="view-component-part visualization-attribute"
          >
            <p id="label-vis-address" className="label-visualization">
              Address
            </p>
            <p id="vs-address" className="class-attribute">
              {this.customerData && this.customerData.address}
            </p>
          </div>
          <div>
            <label htmlFor="input-id-cust">Id Cust</label>
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
      </React.Fragment>
    );
  }
}

export default DetailCustomer;
