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
    const googleLoadTimer = setInterval(() => {
      this.setAuthLoadingStatus(LOADING_STATUS.INITIAL);
      if (window.gapi) {
        this.setAuthLoadingStatus(LOADING_STATUS.LOADING);
        this.loadGoogleAPI(() => {
          clearInterval(googleLoadTimer);
          this.setAuthLoadingStatus(
            LOADING_STATUS.LOADED,
            this.loadAuth2Success
          );
        });
      }
    }, 90);
  };

  componentWillUpdate = async () => {
    console.log(this.state.isAuth);
  };

  // GOOGLE Method

  loadAuth2Success = async () => {
    const token = this.tokenManager.get();

    if (!token) {
      this.logout();
    } else {
      this.checkGoogle(token);
    }
  };

  loadGoogleAPI = func => {
    window.gapi.load('auth2', () => {
      func();
    });
  };

  initializeGoogle = () => {
    return window.gapi.auth2.init({
      client_id: process.env.REACT_APP_GOOGLE_CLIENTID,
    });
  };

  getGoogleAuth = () => {};

  checkGoogle = async token => {
    const googleAuth = await this.initializeGoogle();

    if (googleAuth.isSignedIn.get()) {
      const googleUser = googleAuth.currentUser.get();
      const tokenId = googleUser.getAuthResponse().id_token;

      if (token === tokenId) {
        this.login(tokenId, () => {
          this.setState({ googleAuth });
        });
      } else {
        this.logout();
      }
    }
  };

  loginGoogle = async () => {
    let googleAuth = this.state.googleAuth;

    if (this.state.googleMethod === LOADING_STATUS.LOADED) {
      googleAuth = await this.initializeGoogle();
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

  logoutGoogle = async () => {
    let googleAuth = this.state.googleAuth;

    if (this.state.googleMethod === LOADING_STATUS.LOADED) {
      googleAuth = await this.initializeGoogle();
    }

    googleAuth.signOut();
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

  setAuthLoadingStatus = (status, callback) => {
    this.setState({ googleMethod: status }, callback);
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
