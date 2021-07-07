import React, { useContext, useEffect, useState } from 'react';
import { useHistory } from 'react-router';

import { AuthContext } from '../context/AuthContext';
import { getChatList, OK } from '../api/users'

const ChatsPanel = () => {
    const { tokenPayload, unsetToken } = useContext(AuthContext)
    const history = useHistory()

    const [chats, setChats] = useState([])

    const handleLogoutClick = () => {
        unsetToken()
        history.push('/login')
    }

    const { user } = tokenPayload

    useEffect(() => {
        getChatList(tokenPayload.token).then(([status, data]) => {
            switch (status) {
                case OK:
                    setChats(data.chatlist)
                    break
                default:
                    console.warn("Niebsługiwana akcja");
            }
        })
        .catch(e => console.error(e))

    }, [tokenPayload.token])

    const chatlist = chats.map(chat => (
        <li>
            {chat.name}
        </li>
    ))

    return (
        <div className='friends-panel'>
            <div className='friends-panel__about-user-container'>
                <h3>Zalogowano jako {user}</h3>
                <button
                    className='btn'
                    onClick={handleLogoutClick}>
                    wyloguj
                </button>
            </div>
            <ul className='friends-panel__chatlist'>
                {chatlist}
            </ul>
        </div>
    )
}

export default ChatsPanel