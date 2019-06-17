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
      .map(
        thekey =>
          `${encodeURIComponent(thekey)}=${encodeURIComponent(params[thekey])}`
      )
      .join('&');

    const response = await axios.get(
      `${environment.rootApi}/api/customer/retrieve.abs?${encodedData}`,
      undefined,
      {
        transformRequest: [
          function(data, headers) {
            // Do whatever you want to transform the data
            console.log('data', data, headers);
            return data;
          },
        ],
        maxContentLength: 20000,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          Referer: '',
        },
      }
    );

    return response;
  };
}

export default ApiCustomerRetrieveAbsService;
