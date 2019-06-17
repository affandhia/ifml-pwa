import React from 'react';

class AllAccount extends React.Component {
    state = {};
    componentWillMount = () => {
        this.allAccountData = this.props.jsonAllAccount
    };
    seeDetail = () => {};




    render() {
        return (<li onClick={(e) => { e.preventDefault();
this.seeDetail(); } }>
<div>
    <strong>Account Id</strong>
    <div>{ this.allAccountData && this.allAccountData.id }</div>
    <br/>
</div>
<div>
    <strong>The Account</strong>
    <div>{ this.allAccountData && this.allAccountData.rekening }</div>
    <br/>
</div>
<div>
    <strong>Account Balance</strong>
    <div>{ this.allAccountData && this.allAccountData.balance }</div>
    <br/>
</div>
<hr/>
</li>);
    }
}

export default AllAccount;