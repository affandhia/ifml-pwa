import React from "react";

class Form extends React.Component {
  state = {
    name: "",
    email: "",
    phone: "",
    address: ""
  };

  handleOnSaveBtnClick = e => {
    e.preventDefault();

    const name = this.nameInput.value;
    const phone = this.phoneInput.value;
    const email = this.emailInput.value;
    const address = this.addressInput.value;

    this.props.onSubmit(name, email, phone, address);
  };

  render() {
    return (
      <form>
        <fieldset>
          <legend>Add Customer</legend>
          <div>
            <label htmlFor="input-name">Customer Name</label>
            <div>
              <input
                id="input-name"
                name="name"
                type="text"
                placeholder="type your Name"
                ref={e => { this.nameInput = e }}
              />
            </div>
          </div>
          <div>
            <label htmlFor="input-phone">Customer Phone</label>
            <div>
              <input
                id="input-phone"
                name="phone"
                type="text"
                placeholder="type your Phone"
                ref={e => { this.phoneInput = e }}
              />
            </div>
          </div>
          <div>
            <label htmlFor="input-email">Customer Email</label>
            <div>
              <input
                id="input-email"
                name="email"
                type="text"
                placeholder="type your Email"
                ref={e => { this.emailInput = e }}
              />
            </div>
          </div>
          <div>
            <label htmlFor="input-address">Customer Address</label>
            <div>
              <input
                id="input-address"
                name="address"
                type="text"
                placeholder="type your Address"
                ref={e => { this.addressInput = e }}
              />
            </div>
          </div>
          <div>
            <div>
              <button
                onClick={this.handleOnSaveBtnClick}
                id="button-save"
                name="save"
              >
                Save Customer
              </button>
            </div>
          </div>
        </fieldset>
      </form>
    );
  }
}

export default Form;
