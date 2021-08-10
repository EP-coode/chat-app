import React, { useContext, useEffect, useState } from 'react';
import { Redirect } from 'react-router'

import io from 'socket.io-client'

import ManagePanel from '../components/ManagePanel'
import ChatView from '../components/ChatView'
import { AuthContext } from '../context/AuthContext';
import './UserPanel.css'

function UserPanel() {
    const { tokenPayload } = useContext(AuthContext)
    const [selectedChat, setSelectedChat] = useState({ name: "", id: -1 })
    const [socket, setSocket] = useState(null)

    useEffect(() => {
        if (tokenPayload) {
            const socket = io(`http://localhost:5000?token=${tokenPayload.token}`)
            setSocket(socket)
            return () => socket.close()
        }
    }, [setSocket, tokenPayload])

    if (!tokenPayload)
        return (<Redirect to="/login" />)

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
                    chat_id={selectedChat.id}
                    socket={socket}
                />
            }

        </div>
    )
}

export default UserPanel