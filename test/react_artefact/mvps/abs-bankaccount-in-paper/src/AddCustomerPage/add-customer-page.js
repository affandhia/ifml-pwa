import React from 'react';
import FormAddCustomerComponent from '../FormAddCustomer/form-add-customer.js';

class AddCustomerPage extends React.Component {
    state = {};




    render() {
        return (<React.Fragment>

<FormAddCustomerComponent {...this.props}></FormAddCustomerComponent>

</React.Fragment>);
    }
}

export default AddCustomerPage;