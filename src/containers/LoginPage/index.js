import React from 'react';
import { Redirect } from 'react-router-dom';
import _debounce from 'lodash/debounce';
import { AuthConsumer } from '../Authentication';

class LoginPage extends React.Component {
  saveToken = token => {
    this.props.login(token);
  };

  saveTokenDebounced = _debounce(this.saveToken, 1000);

  handleTokenChange = e => {
    const token = e.target.value;
    this.saveTokenDebounced(token);
  };

  handleLoginWithGoogle = () => {
    this.props.loginGoogle();
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
          <input
            onClick={this.handleLoginWithGoogle}
            value="Login with Google"
            type="button"
          />
          {/* <div id={GOOGLE_BUTTON_ID} /> */}
        </div>
      </div>
    );
  }
}

const withAuth = props => (
  <AuthConsumer>{values => <LoginPage {...props} {...values} />}</AuthConsumer>
);

export default withAuth;
