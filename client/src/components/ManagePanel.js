import React, { useContext, useEffect, useReducer, useState } from 'react';
import { useHistory } from 'react-router';

import { AuthContext } from '../context/AuthContext';
import { getChatList, OK } from '../api/users'
import user_image from '../images/user-icon.png'
import '../App.css'
import './ManagePanel.css'

// const ACTION = {
//     SET_CHATS: 1,
//     SELECT_CHAT: 2,
// }

// const chatListReducer = (state, action) => {
//     switch (action.type) {
//         case ACTION.SET_CHATS:
//             return {
//                 selected_id: state.selected_id,
//                 loaded: true,
//                 chats: action.chats
//             }
//         case ACTION.SELECT_CHAT: {
//             return {
//                 selected_id: action.selected_id,
//                 loaded: state.loaded,
//                 chats: state.chats
//             }
//         }
//         default:
//             throw new Error(`Unexpected action ${action.type}`)
//     }
// }


const ManagePanel = ({ setSelectedChat, selectedChat }) => {
    const { tokenPayload, unsetToken } = useContext(AuthContext)
    const history = useHistory()

    const [chats, setChats] = useState([])

    const handleLogoutClick = () => {
        unsetToken()
        history.push('/login')
    }

    const { user } = tokenPayload

    const handleChatClick = chat => {
        setSelectedChat({ ...chat })
    }

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

    const chatlist = chats.map(chat => {
        let syles = 'manage-panel__chat btn '

        if (chat.id === selectedChat)
            syles += 'manage-panel__chat--active '

        return (
            <li
                className={syles}
                onClick={() => handleChatClick(chat)}
                key={chat.id}>
                <img src={user_image} alt='user icon' className='manage-panel__chat-icon' />
                <p className='manage-panel__chat-name'>{chat.name}</p>
            </li>
        )
    })

    return (
        <div className='manage-panel'>
            <div className='manage-panel__about-user-container'>
                <img src={user_image} alt='user icon' className='manage-panel__user-icon' />
                <h3>Zalogowano jako {user}</h3>
                <button
                    className='manage-panel__logout-btn  btn'
                    onClick={handleLogoutClick}>
                    wyloguj
                </button>
            </div>
            <ul className='manage-panel__chatlist'>
                {chatlist}
            </ul>
            <button
                className='manage-panel__add-friend-btn btn'>
                dodaj znajomego
            </button>
        </div>
    )
}

export default ManagePanel