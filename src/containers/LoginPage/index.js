import React from 'react';
import { Redirect } from 'react-router-dom';
import _debounce from 'lodash/debounce';
import { AuthConsumer } from '../Authentication';

const GOOGLE_BUTTON_ID = 'google-sign-in-button';

class LoginPage extends React.Component {
  componentDidMount = () => {
    window.gapi.signin2.render(GOOGLE_BUTTON_ID, {
      width: 200,
      height: 50,
      onsuccess: this.onSuccess,
    });
  };

  onSuccess = googleUser => {
    // const profile = googleUser.getBasicProfile();
    const id_token = googleUser.getAuthResponse().id_token;
    this.props.login(id_token);
  };

  saveToken = token => {
    this.props.login(token);
  };

  saveTokenDebounced = _debounce(this.saveToken, 1000);

  handleTokenChange = e => {
    const token = e.target.value;
    this.saveTokenDebounced(token);
  };

  render() {
    if (this.props.isAuth) {
      return <Redirect to="/" />;
    }

    return (
      <div>
        <div>Input the Token here</div>
        <div>
          <textarea onChange={this.handleTokenChange} />
        </div>
        <div>- OR -</div>
        <div>
          <button>Login with Google</button>
          <div id={GOOGLE_BUTTON_ID} />
        </div>
      </div>
    );
  }
}

const withAuth = props => (
  <AuthConsumer>{values => <LoginPage {...props} {...values} />}</AuthConsumer>
);

export default withAuth;
