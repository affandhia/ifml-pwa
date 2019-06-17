import React from 'react';
import ApiAccountCreateAbsService from '../services/api-account-create-abs.service';

class NewAccountForm extends React.Component {
    state = {};
    componentWillMount = () => {
        this.existingCustomer = {
            customerId: this.props.idOfTheAccountOwner
        }
    };
    submit = async () => {
        const data = await ApiAccountCreateAbsService.call({
            customerId: this.idOfTheAccountOwnerInput.value,
            rekening: this.theAccountInput.value,
            balance: this.balanceInput.value
        });
    };




    render() {
        return (<form id='new-account-form' >
  <fieldset>
    <legend>New Account Form</legend>
    <div>
    <strong>Customer Id</strong>
    <div>{ this.existingCustomer && this.existingCustomer.customerId }</div>
    <br/>
</div>
<div>
  <label htmlFor="input-id-of-the-account-owner"><strong>Id Of The Account Owner</strong></label>
  <div>
    <input
      id="input-id-of-the-account-owner"
      name="idOfTheAccountOwnerInput"
      type="number"
       placeholder='Fill the Id Of The Account Owner'
       defaultValue={ this.props.idOfTheAccountOwner }
      ref={e => {
        this.idOfTheAccountOwnerInput = e;
      }}
    />
  </div>
  <br/>
</div>
<div>
  <label htmlFor="input-the-account"><strong>The Account</strong></label>
  <div>
    <input
      id="input-the-account"
      name="theAccountInput"
      type="text"
       placeholder='Fill the The Account'
      
      ref={e => {
        this.theAccountInput = e;
      }}
    />
  </div>
  <br/>
</div>
<div>
  <label htmlFor="input-balance"><strong>Balance</strong></label>
  <div>
    <input
      id="input-balance"
      name="balanceInput"
      type="number"
       placeholder='Fill the Balance'
      
      ref={e => {
        this.balanceInput = e;
      }}
    />
  </div>
  <br/>
</div>
        <button
        onClick={(e) => { e.preventDefault();
this.submit(); } }
          name="submit"
          type="submit"
        >
          Submit
        </button>
        
  </fieldset>
</form>);
    }
}

export default NewAccountForm;