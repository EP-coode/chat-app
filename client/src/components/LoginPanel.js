import React, { useContext, useState } from 'react';
import { useHistory } from 'react-router-dom'

import { login, register, OK, CONFILCT, WRONG_CREDENTIALS } from '../api/auth';
import { AuthContext } from '../context/AuthContext';
import './LoginPanel.css'


const LoginPanel = () => {
    const error_style = { color: 'red' }
    const message_style = { color: 'green' }

    const { tokenPayload, setToken } = useContext(AuthContext)

    const history = useHistory()

    if (tokenPayload)
        history.push('/')

    const [loginInput, setLoginInput] = useState('')
    const [passwordInput, setPasswordInput] = useState('')
    const [resoponseMessage, setResponseMessage] = useState({ content: '', style: error_style })

    const onLoginInput = e => {
        setResponseMessage({ content: '', style: error_style })
        setLoginInput(e.target.value)
    }

    const onPasswordInput = e => {
        setResponseMessage({ content: '', style: error_style })
        setPasswordInput(e.target.value)
    }

    const handleLoginClick = e => {
        e.preventDefault()
        login(loginInput, passwordInput).then(([status, response]) => {

            switch (status) {
                case OK:
                    setToken(response.token)
                    break
                case WRONG_CREDENTIALS:
                    setResponseMessage({
                        content: 'Login lub hasło są nieprawidłowe',
                        style: error_style
                    })
                    break
                default:
                    return new Error('Illegal response status')
            }

        }).catch(err => {
            console.error('Nieobsługiwany problem: ', err.message);
        });
    }

    const handleRegisterClick = e => {
        e.preventDefault()
        register(loginInput, passwordInput).then(([status, response]) => {
            switch (status) {
                case OK:
                    setResponseMessage({
                        content: 'Zarejestrowano nowego użytkownika',
                        style: message_style
                    })
                    break
                case CONFILCT:
                    setResponseMessage({
                        content: 'Użytkownik o podanym loginie już figutuje w bazie danych',
                        style: error_style
                    })
                    break
                default:
                    return new Error('Illegal response status')
            }
        }).catch(err => {
            console.warn('Nieobsługiwany problem: ', err.message);
        });
    }

    return (
        <div className="login-panel-container">

            <form className="login-panel">
                <h2 className="login-panel__title">
                    Zaloguj
                </h2>

                <div className="login-panel__input-group">
                    <label
                        className="login-panel__label"
                        htmlFor='login'>
                        Login
                    </label>
                    <input
                        className="login-panel__input"
                        value={loginInput}
                        onInput={onLoginInput}
                        type="text"
                        placeholder="login"
                        name='login'
                    />
                </div>

                <div className="login-panel__input-group">
                    <label
                        className="login-panel__label"
                        htmlFor='password'>
                        Hasło
                    </label>
                    <input
                        className="login-panel__input"
                        value={passwordInput}
                        onInput={onPasswordInput}
                        type="password"
                        placeholder="hasło"
                        name="passwrod"
                    />
                </div>

                <div className="login-panel__btn-container">
                    <button
                        onClick={handleLoginClick}
                        className="login-panel__login-btn btn">
                        Zaloguj
                    </button>

                    <button
                        onClick={handleRegisterClick}
                        className="btn login-panel__register-btn">
                        Zarejestruj
                    </button>
                </div>

                <p className="login-panel__response-box" style={resoponseMessage.style}>
                    {resoponseMessage.content}
                </p>
            </form>
        </div>
    )
}

export default LoginPanel