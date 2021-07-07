import React from 'react';

import './ChatView.css'

function ChatView({ name, user_id }) {
    return (
        <div className='chat'>
            <div className='chat__tilte-container'>
                <h2 className='chat__title'>
                    {name}
                </h2>
            </div>
            <ul className='chat__messages-container'>
                yee
            </ul>
            <div className='chat__typing-container'>
                <input className='chat__text-input' type='text' />
                <button className='btn'>wyślij</button>
            </div>
        </div>
    )
}


export default ChatView