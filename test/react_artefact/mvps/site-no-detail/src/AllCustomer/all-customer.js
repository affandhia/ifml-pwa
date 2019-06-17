import React from 'react';
import queryString from 'query-string';
import ApiCustomerRetrieveAbsService from '../services/api-customer-retrieve-abs.service';
import ApiCustomerDeleteAbsService from '../services/api-customer-delete-abs.service';

class AllCustomer extends React.Component {
  state = {};
  allCustomerData = this.props.jsonAllCustomer || {};
  id = this.allCustomerData.id;
  details = async () => {
    console.log('HEEE', this.props.match.url);
    Object.defineProperty(document, 'referer', {
      get: function() {
        return this.props.match.url;
      },
    });

    const data = await ApiCustomerRetrieveAbsService.call({
      id: this.idInput.value,
    });

    this.props.history.push({
      pathname: '/customer-page/customer-content/detail-customer-page',
      search: queryString.stringify({
        objectDetailCustomer: JSON.stringify(data['data']['data']),
      }),
    });
  };
  delete = async () => {
    const data = await ApiCustomerDeleteAbsService.call({
      id: this.idInput.value,
    });
  };

  render() {
    return (
      <li>
        <div
          id="div-vis-customer-id"
          className="view-component-part visualization-attribute"
        >
          <p id="label-vis-customer-id" className="label-visualization">
            Customer Id
          </p>
          <p id="vs-customer-id" className="class-attribute">
            {this.allCustomerData && this.allCustomerData.id}
          </p>
        </div>
        <div
          id="div-vis-customer-name"
          className="view-component-part visualization-attribute"
        >
          <p id="label-vis-customer-name" className="label-visualization">
            Customer Name
          </p>
          <p id="vs-customer-name" className="class-attribute">
            {this.allCustomerData && this.allCustomerData.name}
          </p>
        </div>
        <div>
          <label htmlFor="input-id">Id</label>
          <div>
            <input
              id="input-id"
              name="idInput"
              type="number"
              placeholder="Fill the Id"
              defaultValue={this.allCustomerData.id}
              ref={e => {
                this.idInput = e;
              }}
            />
          </div>
        </div>
        <button
          onClick={e => {
            e.preventDefault();
            this.details();
          }}
        >
          Details
        </button>
        <button
          onClick={e => {
            e.preventDefault();
            this.delete();
          }}
        >
          Delete
        </button>
      </li>
    );
  }
}

export default AllCustomer;
