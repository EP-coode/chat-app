import React, { useContext } from 'react';

import { AuthContext } from '../context/AuthContext'

function UserPanel() {
    const { unsetToken } = useContext(AuthContext)


    return (
        <div className='user-panel'>
            yee
            <button
                className='btn'
                onClick={unsetToken}>
                wyloguj
            </button>
        </div>
    )
}

export default UserPanel