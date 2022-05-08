import React, { useEffect, useCallback } from 'react'
import { Switch, Route, useHistory, useLocation } from 'react-router-dom'
import ProtectedRoutes from './route/protected_route'
import AuthRoutes from './route/auth_route'
import { NotMatch404 } from './views/error/NotMatch404'
import { checkTokenExists } from './auth.js'

export default function App() {
    const history = useHistory()
    const { search } = useLocation()

    const checkUserAuth = useCallback(() => {
        let filter_prefix = String(history.location.pathname.split('/', 2))
        let prefix = filter_prefix.replace(',', '/')
        let current_access_path = history.location.pathname + search
        if (prefix === '/session' && search.length > 0) {
            history.push(current_access_path)
        } else if (prefix === '/session' && search.length < 1) {
            current_access_path === '/' ? history.push('/session/login') : history.push(current_access_path)
        } else {
            const fetchUserAuth = async () => {
                if (!checkTokenExists()) {
                    history.push('/session/login')
                } else {
                    current_access_path === '/' ? history.push('/user/ptt') : history.push(current_access_path)
                }
            }
            fetchUserAuth()
        }
    }, [history, search])

    useEffect(() => {
        checkUserAuth()
    }, [checkUserAuth])

    return (
        <Switch>
            <Route path="/404" component={NotMatch404} />
            <Route path="/session" render={(props) => <AuthRoutes {...props} />} />
            <Route exect path="/user" render={(props) => <ProtectedRoutes {...props} />} />
        </Switch>
    )
}
