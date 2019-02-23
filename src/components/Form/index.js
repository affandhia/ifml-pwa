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
    const {
      name,
      phone,
      email,
      address,
      buttonText,
    } = this.props;

    return (
      <form>
        <fieldset>
          <legend>{this.props.formTitle}</legend>
          <div>
            <label htmlFor="input-name">Customer Name</label>
            <div>
              <input
                id="input-name"
                name="name"
                type="text"
                placeholder="type your Name"
                defaultValue={name}
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
                defaultValue={phone}
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
                defaultValue={email}
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
                defaultValue={address}
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
                {buttonText}
              </button>
            </div>
          </div>
        </fieldset>
      </form>
    );
  }
}

Form.defaultProps = {
  formTitle: 'Form',
  buttonText: 'Submit',
}

export default Form;
