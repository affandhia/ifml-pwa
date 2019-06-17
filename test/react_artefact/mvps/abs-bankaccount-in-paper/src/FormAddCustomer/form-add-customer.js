import React from 'react';
import queryString from 'query-string';
import ApiCustomerCreateAbsService from '../services/api-customer-create-abs.service';

class FormAddCustomer extends React.Component {
    state = {};
    save = async () => {
        const data = await ApiCustomerCreateAbsService.call({
            name: this.customerNameInput.value,
            email: this.customerEmailInput.value,
            phone: this.customerPhoneInput.value,
            address: this.customerAddressInput.value
        });

        this.props.history.push({
            pathname: '/customer-page/customer-content/list-customer-page',
            search: queryString.stringify({
                jsonAllCustomer: JSON.stringify(data['data']['data'])
            })
        });
    };




    render() {
        return (<form id='form-add-customer' >
  <fieldset>
    <legend>Form Add Customer</legend>
    <div>
  <label htmlFor="input-customer-name"><strong>Customer Name</strong></label>
  <div>
    <input
      id="input-customer-name"
      name="customerNameInput"
      type="text"
       placeholder='Fill the Customer Name'
      
      ref={e => {
        this.customerNameInput = e;
      }}
    />
  </div>
  <br/>
</div>
<div>
  <label htmlFor="input-customer-phone"><strong>Customer Phone</strong></label>
  <div>
    <input
      id="input-customer-phone"
      name="customerPhoneInput"
      type="text"
       placeholder='Fill the Customer Phone'
      
      ref={e => {
        this.customerPhoneInput = e;
      }}
    />
  </div>
  <br/>
</div>
<div>
  <label htmlFor="input-customer-email"><strong>Customer Email</strong></label>
  <div>
    <input
      id="input-customer-email"
      name="customerEmailInput"
      type="text"
       placeholder='Fill the Customer Email'
      
      ref={e => {
        this.customerEmailInput = e;
      }}
    />
  </div>
  <br/>
</div>
<div>
  <label htmlFor="input-customer-address"><strong>Customer Address</strong></label>
  <div>
    <input
      id="input-customer-address"
      name="customerAddressInput"
      type="text"
       placeholder='Fill the Customer Address'
      
      ref={e => {
        this.customerAddressInput = e;
      }}
    />
  </div>
  <br/>
</div>
        <button
        onClick={(e) => { e.preventDefault();
this.save(); } }
          name="save"
          type="submit"
        >
          Save
        </button>
        
  </fieldset>
</form>);
    }
}

export default FormAddCustomer;