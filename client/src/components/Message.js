import React from 'react';

import './Message.css'

function Message({ sender_name, content, readed, date, isMine}){
    const wrepper_classes = `message ${isMine && 'message--my'}`
    return(
        <div className={wrepper_classes}>
            <h3>{sender_name}</h3>
            <p>{content}</p>
            <p className="message__date">{date}</p>
        </div>
    )
}

export default Message