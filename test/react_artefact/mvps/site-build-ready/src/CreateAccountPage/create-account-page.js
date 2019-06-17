import React from 'react';
import queryString from 'query-string';
import NewAccountFormComponent from '../NewAccountForm/new-account-form.js';

class CreateAccountPage extends React.Component {
  state = {};
  componentDidMount = () => {
    this.setState({
      idOfTheAccountOwner: JSON.parse(
        queryString.parse(this.props.location.search).idOfTheAccountOwner
      ),
    });
  };

  render() {
    return (
      <React.Fragment>
        {this.state.idOfTheAccountOwner !== undefined && (
          <NewAccountFormComponent
            {...this.props}
            idOfTheAccountOwner={this.state.idOfTheAccountOwner}
          />
        )}
      </React.Fragment>
    );
  }
}

export default CreateAccountPage;
