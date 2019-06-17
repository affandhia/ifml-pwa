import React from 'react';
import queryString from 'query-string';
import AllAccountComponent from '../AllAccount/all-account.js';

class AllAccountPage extends React.Component {
  state = {};
  componentDidMount = () => {
    this.setState({
      jsonAllAccount: JSON.parse(
        queryString.parse(this.props.location.search).jsonAllAccount
      ),
    });
  };

  render() {
    return (
      <React.Fragment>
        <ul
          id="list-AllAccountComponent"
          className="list-component view-component"
        >
          {this.state.jsonAllAccount &&
            this.state.jsonAllAccount.map(jsonAllAccount => (
              <AllAccountComponent
                {...this.props}
                jsonAllAccount={jsonAllAccount}
              />
            ))}
        </ul>
      </React.Fragment>
    );
  }
}

export default AllAccountPage;
