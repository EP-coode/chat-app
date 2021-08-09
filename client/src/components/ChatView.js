import React, { useEffect, useContext, useState, useRef } from 'react';

import { AuthContext } from '../context/AuthContext';
import { getMessagesFromChat, sendMessage } from '../api/chating'
import Message from './Message'
import './ChatView.css'

function ChatView({ name, chat_id }) {
    const { tokenPayload } = useContext(AuthContext)
    const messageInput = useRef(null)
    
    const [ messages, setMessages ] = useState([])
    useEffect(() => {
       reloadMessages()
    }, [tokenPayload.token, chat_id])

    const reloadMessages = () => {
        getMessagesFromChat(tokenPayload.token, chat_id).then(([status, data]) => {
            console.log(data);
            setMessages(data.messages)
        })
    }

    const handleSend = () => {
        const message = messageInput.current.value
        if(message)
        {
            sendMessage(tokenPayload.token, chat_id, message).then(([status, data]) => {
                console.log(data) 
            })
            messageInput.current.value = ""
        }
    }

  
    const messagesComp = messages.map(msg => {
            return (
                <Message
                    sender_name={msg.sender_name}
                    content={msg.content}
                    date={msg.send_time}
                    isMine={tokenPayload.user == msg.sender_name}
                />
            )
    })

    return (
        <div className='chat'>
            <div className='chat__tilte-container'>
                <h2 className='chat__title'>
                    {name}
                </h2>
            </div>
            <ul className='chat__messages-container'>
                {messagesComp}
            </ul>
            <div className='chat__typing-container'>
                <input className='chat__text-input' type='text' ref={messageInput} />
                <button className='btn' onClick={handleSend}>wyślij</button>
                <button className='btn' onClick={reloadMessages}>załaduj</button>
            </div>
        </div>
    )
}


export default ChatView