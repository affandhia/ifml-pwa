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
        this.initGoogle(() => {
          clearInterval(googleLoadTimer);
          this.setAuthLoadingStatus(LOADING_STATUS.LOADED);
        });
      }
    }, 90);
  };

  login = token => {
    this.tokenManager.set(token);

    this.setState({
      isAuth: true,
    });
  };

  logout = () => {
    this.tokenManager.clear();

    window.gapi.auth2.getAuthInstance().signOut();

    this.setState({ isAuth: false });
  };

  initGoogle = func => {
    window.gapi.load('auth2', function() {
      window.gapi.auth2
        .init({
          client_id: process.env.REACT_APP_GOOGLE_CLIENTID,
        })
        .then(func);
    });
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
          logout: this.logout,
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
