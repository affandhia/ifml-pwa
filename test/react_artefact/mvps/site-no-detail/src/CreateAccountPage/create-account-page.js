import React from 'react';
import queryString from 'query-string';
import NewAccountFormComponent from '../NewAccountForm/new-account-form.js';

class CreateAccountPage extends React.Component {
  state = {};
  idOfTheAccountOwner;
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
        <NewAccountFormComponent
          {...this.props}
          idOfTheAccountOwner={this.state.idOfTheAccountOwner}
        />
      </React.Fragment>
    );
  }
}

export default CreateAccountPage;
