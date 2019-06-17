import React from 'react';
import ApiAccountCreateAbsService from '../services/api-account-create-abs.service';

class NewAccountForm extends React.Component {
  state = {};
  existingCustomer = {
    customerId: this.props.idOfTheAccountOwner,
  };
  submit = async () => {
    const data = await ApiAccountCreateAbsService.call({
      customerId: this.idOfTheAccountOwnerInput.value,
      rekening: this.theAccountInput.value,
      balance: this.balanceInput.value,
    });
  };

  render() {
    return (
      <form id="new-account-form">
        <fieldset>
          <legend>New Account Form</legend>
          <div
            id="div-vis-customer-id"
            className="view-component-part visualization-attribute"
          >
            <p id="label-vis-customer-id" className="label-visualization">
              Customer Id
            </p>
            <p id="vs-customer-id" className="class-attribute">
              {this.existingCustomer['customerId']}
              {JSON.stringify(this.existingCustomer)}
            </p>
          </div>
          <div>
            <label htmlFor="input-id-of-the-account-owner">
              Id Of The Account Owner
            </label>
            <div>
              <input
                id="input-id-of-the-account-owner"
                name="idOfTheAccountOwnerInput"
                type="number"
                placeholder="Fill the Id Of The Account Owner"
                ref={e => {
                  this.idOfTheAccountOwnerInput = e;
                }}
              />
            </div>
          </div>
          <div>
            <label htmlFor="input-the-account">The Account</label>
            <div>
              <input
                id="input-the-account"
                name="theAccountInput"
                type="text"
                placeholder="Fill the The Account"
                ref={e => {
                  this.theAccountInput = e;
                }}
              />
            </div>
          </div>
          <div>
            <label htmlFor="input-balance">Balance</label>
            <div>
              <input
                id="input-balance"
                name="balanceInput"
                type="number"
                placeholder="Fill the Balance"
                ref={e => {
                  this.balanceInput = e;
                }}
              />
            </div>
          </div>
          <button
            onClick={this.submit}
            id="button-submit"
            name="submit"
            type="submit"
          >
            Submit
          </button>
        </fieldset>
      </form>
    );
  }
}

export default NewAccountForm;
