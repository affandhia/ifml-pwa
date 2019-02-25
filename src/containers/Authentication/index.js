import React from 'react';
import { Redirect } from 'react-router-dom';
import Token from '../../utils/token';

const AuthContext = React.createContext();

export const LOADING_STATUS = {
  INITIAL: 'INITIAL',
  LOADING: 'LOADING',
  LOADED: 'LOADED',
  FAILED: 'FAILED',
};

export class AuthProvider extends React.Component {
  state = { isAuth: false, googleMethod: null };
  tokenManager = new Token();

  componentDidMount = () => {
    const token = this.tokenManager.get();
    if (!token) {
      this.logout();
      return;
    }

    const googleLoadTimer = setInterval(() => {
      this.setAuthLoadingStatus(LOADING_STATUS.INITIAL);
      if (window.gapi) {
        this.setAuthLoadingStatus(LOADING_STATUS.LOADING);
        this.initGoogle(googleAuth => {
          clearInterval(googleLoadTimer);
          this.checkGoogle(googleAuth);
        });
      }
    }, 90);
  };

  componentWillUpdate = () => {
    console.log(this.state.isAuth);
  };

  // GOOGLE Method

  initGoogle = func => {
    window.gapi.load('auth2', function() {
      window.gapi.auth2
        .init({
          client_id: process.env.REACT_APP_GOOGLE_CLIENTID,
        })
        .then(func);
    });
  };

  getGoogleAuth = () => {};

  checkGoogle = googleAuth => {
    if (googleAuth.isSignedIn.get()) {
      const googleUser = googleAuth.currentUser.get();
      const tokenId = googleUser.getAuthResponse().id_token;
      this.login(tokenId, () => {
        this.setState({ googleAuth }, () =>
          this.setAuthLoadingStatus(LOADING_STATUS.LOADED)
        );
      });
      return;
    }

    this.setState({ googleAuth }, () =>
      this.setAuthLoadingStatus(LOADING_STATUS.LOADED)
    );
  };

  loginGoogle = () => {
    const googleAuth = this.state.googleAuth;
    if (!googleAuth) {
      this.initGoogle(this.loginGoogleHelper);
      return;
    }

    this.loginGoogleHelper(googleAuth);
  };

  loginGoogleHelper = googleAuth => {
    googleAuth
      .signIn({
        scope: 'profile email',
      })
      .then(googleUser => {
        const tokenId = googleUser.getAuthResponse().id_token;

        this.login(tokenId);
      });
  };

  logoutGoogle = () => {
    const googleAuth = this.state.googleAuth;
    if (!googleAuth) {
      this.initGoogle(auth => {
        this.setAuthLoadingStatus(LOADING_STATUS.LOADED);
        auth.signOut();
      });
    } else {
      googleAuth.signOut();
    }
  };

  // [END] GOOGLE Method

  login = (token, callback) => {
    this.tokenManager.set(token);

    this.setState(
      {
        isAuth: true,
      },
      callback
    );
  };

  logout = () => {
    this.tokenManager.clear();

    // logout vendor
    this.logoutGoogle();
    // end

    this.setState({ isAuth: false });
  };

  setAuthLoadingStatus = status => {
    this.setState({ googleMethod: status });
  };

  render() {
    if (this.state.googleMethod !== LOADING_STATUS.LOADED) {
      return null;
    }

    return (
      <AuthContext.Provider
        value={{
          isAuth: this.state.isAuth,
          login: this.login,
          loginGoogle: this.loginGoogle,
          logout: this.logout,
          gapi: window.gapi,
        }}
      >
        {this.props.children}
      </AuthContext.Provider>
    );
  }
}

export const AuthConsumer = AuthContext.Consumer;

export const withAuth = ComposedComponent => {
  return class extends React.Component {
    render() {
      return (
        <AuthConsumer>
          {value =>
            value.isAuth ? (
              <ComposedComponent {...this.props} {...value} />
            ) : (
              <Redirect to="/login" />
            )
          }
        </AuthConsumer>
      );
    }
  };
};

export default AuthContext;
