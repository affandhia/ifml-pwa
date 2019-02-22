import React from "react";
import { Link } from "react-router-dom";

class Navbar extends React.Component {
  render() {
    const { match } = this.props;

    return (
      <ul>
        <li>
          <Link
            to={`${
              match.url.endsWith("/") ? `${match.url}add` : `${match.url}/add`
            }`}
          >
            Add Customer
          </Link>
        </li>
        <li>
          <Link to={match.url}>List Customer</Link>
        </li>
      </ul>
    );
  }
}

export default Navbar;
