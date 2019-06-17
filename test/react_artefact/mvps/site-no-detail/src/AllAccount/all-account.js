import React from 'react';

class AllAccount extends React.Component {
  state = {};
  allAccountData = this.props.jsonAllAccount || {};
  seeDetail = () => {};

  render() {
    return (
      <li
        onClick={e => {
          e.preventDefault();
          this.seeDetail();
        }}
      >
        <div
          id="div-vis-account-id"
          className="view-component-part visualization-attribute"
        >
          <p id="label-vis-account-id" className="label-visualization">
            Account Id
          </p>
          <p id="vs-account-id" className="class-attribute">
            {this.allAccountData && this.allAccountData.id}
          </p>
        </div>
        <div
          id="div-vis-the-account"
          className="view-component-part visualization-attribute"
        >
          <p id="label-vis-the-account" className="label-visualization">
            The Account
          </p>
          <p id="vs-the-account" className="class-attribute">
            {this.allAccountData && this.allAccountData.rekening}
          </p>
        </div>
        <div
          id="div-vis-account-balance"
          className="view-component-part visualization-attribute"
        >
          <p id="label-vis-account-balance" className="label-visualization">
            Account Balance
          </p>
          <p id="vs-account-balance" className="class-attribute">
            {this.allAccountData && this.allAccountData.balance}
          </p>
        </div>
      </li>
    );
  }
}

export default AllAccount;
