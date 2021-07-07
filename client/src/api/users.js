export const OK = 1
export const WRONG_CREDENTIALS = 2
export const IVITATION_ALREADY_EXIST = 3
export const NO_SUCH_INVITATION = 4

export const getChatList = async token => {
    const response = await fetch('http://localhost:5000/chat',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.json()]
}

export const getUserList = async token => {
    const response = await fetch('http://localhost:5000/users', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.json()]
}


export const sendIvitation = async (token, user_id) =>{
    const response = await fetch('http://localhost:5000/invitate', {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id
        }),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]
    
    if (response.status === 400)
        return [IVITATION_ALREADY_EXIST, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.text()]
}


export const getPendingIvitations = async token => {
    const response = await fetch('http://localhost:5000/invitate', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token.toStrong()
        }
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.json()]
}


export const acceptIvitation = async (token, user_id) => {
    const response = await fetch('http://localhost:5000/invitate/accept', {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id
        }),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token.toStrong()
        }
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.json()]
}