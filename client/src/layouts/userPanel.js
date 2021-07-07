import React, { useContext } from 'react';
import { Redirect, useHistory } from 'react-router'

import ChatsPanel from '../components/ChatsPanel'
import { AuthContext } from '../context/AuthContext';

function UserPanel() {
    const { tokenPayload } = useContext(AuthContext)

    if (!tokenPayload)
        return (<Redirect to="/login"/>)

    return (
        <div className='user-panel'>
            <ChatsPanel />
        </div>
    )
}

export default UserPanel