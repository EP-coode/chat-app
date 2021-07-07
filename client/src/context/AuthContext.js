import React, { useState } from 'react';
import jwt_decode from 'jwt-decode'

export const AuthContext = React.createContext()

const AuthProvider = ({ children }) => {
    const [tokenPayload, setTokenPayload] = useState(null)

    const setToken = token =>{
        const decoded = jwt_decode(token)
        setTokenPayload({...decoded, token})
    }

    const unsetToken = () =>{
        setTokenPayload(null)
    }

    return(
        <AuthContext.Provider 
            value={{
                tokenPayload,
                setToken,
                unsetToken
            }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthProvider