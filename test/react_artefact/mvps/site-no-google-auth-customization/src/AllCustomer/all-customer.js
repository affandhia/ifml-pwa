import React from 'react';
import queryString from 'query-string';
import ApiCustomerRetrieveAbsService from '../services/api-customer-retrieve-abs.service';
import ApiCustomerDeleteAbsService from '../services/api-customer-delete-abs.service';

class AllCustomer extends React.Component {
  state = {};
  componentWillMount = () => {
    this.allCustomerData = this.props.jsonAllCustomer || {};
    this.id = this.allCustomerData.id;
  };
  details = async () => {
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
        <div>
          <strong>Customer Id</strong>
          <div>{this.allCustomerData && this.allCustomerData.id}</div>
          <br />
        </div>
        <div>
          <strong>Customer Name</strong>
          <div>{this.allCustomerData && this.allCustomerData.name}</div>
          <br />
        </div>
        <div>
          <label htmlFor="input-id">
            <strong>Id</strong>
          </label>
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
          <br />
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
        <hr />
      </li>
    );
  }
}

export default AllCustomer;
