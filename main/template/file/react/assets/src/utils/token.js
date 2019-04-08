import { Cookies } from 'react-cookie';

class Token {
  cookies = new Cookies();

  get() {
    const token = this.cookies.get('token');

    return token;
  }

  set(token) {
    this.cookies.set('token', token, { path: '/' });
  }

  clear() {
    this.cookies.remove('token');
  }
}

export default Token;
