import React from 'react';
import { Link } from 'react-router-dom';

class Navbar extends React.Component {
    render() {
        return (
            <ul>
                <li><Link to="/customer">Customer</Link></li>
                <li><Link to="/account">Account</Link></li>
            </ul>
        )
    }
}

export default Navbar;