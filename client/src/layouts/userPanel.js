import React, { useContext, useState } from 'react';
import { Redirect } from 'react-router'

import ManagePanel from '../components/ManagePanel'
import ChatView from '../components/ChatView'
import { AuthContext } from '../context/AuthContext';
import './UserPanel.css'

function UserPanel() {
    const { tokenPayload } = useContext(AuthContext)
    const [ selectedChat, setSelectedChat] = useState({name: "", id: -1})

    if (!tokenPayload)
        return (<Redirect to="/login"/>)

    return (
        <div className='user-panel'>
            <ManagePanel 
                setSelectedChat={setSelectedChat}
                selectedChat={selectedChat}
            />
            {
                selectedChat.id > 0 &&
                <ChatView
                    name={selectedChat.name}
                    user_id={selectedChat.id}
                />
            }   

        </div>
    )
}

export default UserPanel