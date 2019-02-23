import React from "react";
import axios, { CancelToken } from "axios";
import { Link } from "react-router-dom";

import Form from "../../components/Form";

import Token from "../../utils/token";

class DetailCustomerPage extends React.Component {
  state = {
    source: CancelToken.source(),
    data: {},
    loading: false,
    error: null,
  };
  _isMounted = false;

  componentDidMount = () => {
    this._isMounted = true;
    const { match } = this.props;

    this.getCustomerDetail(match.params.id);
  };

  componentWillUnmount = () => {
    this._isMounted = false;

    this.state.source.cancel(
      "Operation canceled because of the component will be unmounted"
    );
  };

  getCustomerDetail = async id => {
    const token = new Token().get();

    const encodedData = `id=${encodeURI(id)}`;

    this.setState({
      loading: true,
      data: {}
    });

    try {
      const response = await axios.get(
        `http://localhost:8089/api/customer/retrieve.abs?token=${token}&${encodedData}`,
        undefined,
        {
          cancelToken: this.state.source
        }
      );

      if (this._isMounted) {
        this.setState({
          loading: false,
          error: null,
          data: response.data.data
        });
      }
    } catch (e) {
      console.log(e);
      this.setState({
        loading: false,
        error: 'The customer ID can not be found',
        data: {}
      });
    }
  };

  render() {
    const { id, name, email, phone, address } = this.state.data;

    if (this.state.loading) {
      return <div>Loading the detail...</div>;
    }

    return (
      <div>
          <div>
          <Link to="/customer">
            <button>Back to List</button>
          </Link>
        </div>

        {this.state.error ? <div>{this.state.error}</div> : <Form
          name={name}
          email={email}
          phone={phone}
          address={address}
          formTitle={`Detail Customer #${id}`}
          hideSubmitButton
          onSubmit={() => {}}
        />}

        
      </div>
    );
  }
}

export default DetailCustomerPage;
