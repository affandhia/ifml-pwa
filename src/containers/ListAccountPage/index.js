import React from 'react';
import axios, { CancelToken } from 'axios';

import { withAuth } from '../Authentication';

import Token from '../../utils/token';

class ListAccountPage extends React.Component {
  state = {
    list: [],
    loading: null,
    source: CancelToken.source(),
  };
  _isMounted = false;

  componentDidMount() {
    this._isMounted = true;

    this.getList();
  }

  componentWillUnmount() {
    this._isMounted = false;

    this.state.source.cancel(
      'Operation canceled because of the component will be unmounted'
    );
  }

  getList = async (token = '') => {
    token = token ? token : new Token().get();

    try {
      const response = await axios.get(
        `/api/account/list.abs?token=${token}`,
        undefined,
        {
          cancelToken: this.state.source,
        }
      );

      if (this._isMounted) {
        this.setState({
          list: response.data.data,
        });
      }
    } catch (e) {
      console.log(e);
    }
  };

  renderData = (data) => {
    const keys = Object.keys(data);
    return (<React.Fragment>
      {keys.map(key => <div key={key}>{key}: {data[key]}</div>)}
    </React.Fragment>);
  }

  renderList = () => {
    const { list } = this.state;

    return (
      <React.Fragment>
        {list.map(data => {
          return (
            <li key={data.id}>
              {this.renderData(data)}
            </li>
          );
        })}
      </React.Fragment>
    );
  };

  render() {
    return (
      <React.Fragment>
        {this.state.loading ? <div>{this.state.loading}</div> : null}
        <ul>{this.renderList()}</ul>
      </React.Fragment>
    );
  }
}

export default withAuth(ListAccountPage);
