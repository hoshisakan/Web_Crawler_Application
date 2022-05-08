import React, { useEffect, useCallback } from 'react'
import { useHistory } from 'react-router-dom'
import { checkTokenExists, removeAllLocalStorage } from '../../auth'
import { apiLogoutRevokeToken } from '../../api.js'

export default function LogoutPage() {
    const history = useHistory()

    const handleUserLogout = useCallback(() => {
        const revokeToken = async () => {
            let data = {
                refresh: localStorage.getItem('refresh_token'),
            }
            apiLogoutRevokeToken(data)
                .then((res) => {
                    removeAllLocalStorage()
                    if (!checkTokenExists() && res.data['allow_logout'] === true) {
                        history.push('/session/login')
                    }
                })
                .catch((err) => {
                    // console.error(err)
                    removeAllLocalStorage()
                    history.push('/session/login')
                })
        }
        revokeToken()
    }, [history])

    useEffect(() => {
        handleUserLogout()
    }, [handleUserLogout])

    return <div></div>
}
