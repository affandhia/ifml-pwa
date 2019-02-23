import React from 'react';
import { Redirect } from 'react-router-dom';
import Token from '../../utils/token';

const AuthContext = React.createContext();

export class AuthProvider extends React.Component {
  state = { isAuth: false };
  tokenManager = new Token();

  login = token => {
    this.tokenManager.set(token);

    this.setState({
      isAuth: true,
    });
  };

  logout = () => {
    this.setState({ isAuth: false });
    this.tokenManager.clear();
  };

  render() {
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
