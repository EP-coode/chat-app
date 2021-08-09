export const OK = 1
export const WRONG_CREDENTIALS = 2
export const IVITATION_ALREADY_EXIST = 3
export const NO_SUCH_INVITATION = 4


export const getMessagesFromChat = async (token, chat_id) => {
    const response = await fetch(`http://localhost:5000/message?chat_id=${chat_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token.toString()
        },
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.json()]
}


export const sendMessage = async (token, chat_id, content) => {
    const response = await fetch('http://localhost:5000/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token.toString()
        },
        body: JSON.stringify({
            target: chat_id,
            content,
        })
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.text()]
}