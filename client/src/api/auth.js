export const OK = 1
export const WRONG_CREDENTIALS = 2
export const CONFILCT = 3

export const login = async (login = '', password = '') => {
    const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        body: JSON.stringify({
            login: login,
            password: password
        }),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })

    if (response.status === 403)
        return [WRONG_CREDENTIALS, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.json()]
}

export const register = async (login = '', password = '') => {
    const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        body: JSON.stringify({
            login: login,
            password: password
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    })

    if (response.status === 409)
        return [CONFILCT, await response.text()]

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return [OK, await response.text()]
}