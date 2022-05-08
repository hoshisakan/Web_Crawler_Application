import React, { useEffect, useCallback, useState, useRef } from 'react'
import { Route, Redirect, useHistory } from 'react-router-dom'
import { UserRouter } from './routes'
import UserHeader from '../components/Navbars/UserHeader'
import '../assets/css/protected_page_style.css'
import useInterval from '../components/Timer/useInterval'
import { checkTokenExists, removeAllLocalStorage } from '../auth'
import { apiRefreshToken, apiUpdateUserProfile, apiTokenExpireCheck, apiLogoutRevokeToken } from '../api.js'
import { getCurrentWindowSize } from '../assets/js/getWindowSize.js'


export default function ProtectedRoutes(props) {
    const history = useHistory()
    const mainPanel = useRef(null)
    const [allowRender, setAllowRender] = useState(false)
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [checkTokenExpireTime, setCheckTokenExpireTime] = useState(60000) // default check token epxire time 1 minutes
    const currentWindowSize = getCurrentWindowSize()
    
    const getRoutes = (routes) => {
        let route = null
        let index = 0
        for (let prop of routes) {
            if (prop.path_prefix === '/user' && history.location.pathname === prop.path_prefix + prop.path) {
                if (prop.path === '/profile') {
                    route = (
                    <Route
                        path={prop.path_prefix + prop.path}
                        render={(props) => <prop.component username={username} email={email} />}
                        key={index}
                    />
                )
                } else {
                    route = (
                    <Route
                        path={prop.path_prefix + prop.path}
                        render={(props) => <prop.component {...props} currentWindowSize={currentWindowSize} />}
                        key={index}
                    />
                )
                }
                break
            }
            index++
        }
        index = 0
        return route
    }

    const checkUserAuth = useCallback(() => {
        const fetchUserProfile = async () => {
            if (username.length < 1 || username === '' || email.length < 1 || email === '') {
                await apiUpdateUserProfile()
                    .then((res) => {
                        let res_data = res.data.info
                        setUsername(res_data['user'])
                        setEmail(res_data['email'])
                    })
                    .catch((err) => {
                    })
            }
        }
        const refreshTokenRequest = async () => {
            let data = {
                refresh: localStorage.getItem('refresh_token'),
            }
            await apiRefreshToken(data)
                .then((res) => {
                    localStorage.setItem('access_token', res.data['access'])
                    setAllowRender(true)
                    fetchUserProfile()
                })
                .catch((err) => {
                    setAllowRender(false)
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
                })
        }
        const fetchUserAuth = async () => {
            await apiTokenExpireCheck()
                .then((res) => {
                    let data = res.data
                    let token_time_left = data['token_time_left']
                    if (token_time_left > 60) {
                        setCheckTokenExpireTime(60000)
                    } else if (token_time_left === 60) {
                        setCheckTokenExpireTime(20000)
                    } else if (token_time_left >= 30 && token_time_left <= 60) {
                        setCheckTokenExpireTime(10000)
                    } else if (token_time_left <= 30) {
                        refreshTokenRequest()
                    }
                    setAllowRender(true)
                    fetchUserProfile()
                })
                .catch((err) => {
                    refreshTokenRequest()
                })
        }
        fetchUserAuth()
    }, [email, history, username])

    const renderRoute = getRoutes(UserRouter)

    useInterval(() => {
        checkUserAuth()
    }, checkTokenExpireTime)

    useEffect(() => {
        checkUserAuth()
    }, [checkUserAuth])

    return (
        <div>
            <div className="wrapper">
                <div className="mainPanel" ref={mainPanel}>
                    {allowRender ? (
                        renderRoute === null ? (
                            <Redirect to="/404" />
                        ) : (
                            <div>
                                <UserHeader username={username} currentWindowSize={currentWindowSize} />
                                {renderRoute}
                            </div>
                        )
                    ) : null}
                </div>
            </div>
        </div>
    )
}
