import React from "react";

class Form extends React.Component {
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
              />
            </div>
          </div>
          <div>
            <div>
              <button id="button-save" name="save">
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
