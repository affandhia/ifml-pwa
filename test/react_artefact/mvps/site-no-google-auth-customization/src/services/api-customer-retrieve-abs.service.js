import axios from 'axios';
import Token from '../utils/token';
import environment from '../utils/environment';

class ApiCustomerRetrieveAbsService {
  static call = async (params = {}) => {
    const token = new Token().get();
    params = Object.assign(params, {
      token,
    });

    const encodedData = Object.keys(params)
      .map(thekey => `${thekey}=${encodeURI(params[thekey])}`)
      .join('&');

    try {
      const response = await axios.get(
        `${environment.rootApi}/api/customer/retrieve.abs?${encodedData}`
      );

      return response;
    } catch (e) {
      return {};
    }
  };
}

export default ApiCustomerRetrieveAbsService;