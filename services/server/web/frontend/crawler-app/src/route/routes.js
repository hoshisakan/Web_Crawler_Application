import UserProfile from '../views/user/UserProfile'
import LoginPage from '../views/user/LoginPage'
import LogoutPage from '../views/user/LogoutPage'
import RegisterPage from '../views/user/RegisterPage'
import ApplyResetPasswordPage from '../views/user/ApplyResetPasswordPage'
import ResetPasswordPage from '../views/user/ResetPasswordPage'
import RegisterValidatePage from '../views/user/RegisterValidatePage'
import GoogleSearchInfo from '../views/google_search/Search'
import StcokSearch from '../views/stock/Search'
import PttSearch from '../views/ptt/Search'


export const UserRouter = [
    {
        path: '/google-search',
        name: 'GoogleSearch',
        icon: '',
        component: GoogleSearchInfo,
        path_prefix: '/user',
    },
    {
        path: '/stock',
        name: 'Stock',
        icon: '',
        component: StcokSearch,
        path_prefix: '/user',
    },
    {
        path: '/ptt',
        name: 'Ptt',
        icon: '',
        component: PttSearch,
        path_prefix: '/user',
    },
    {
        path: '/profile',
        name: 'UserProfile',
        icon: '',
        component: UserProfile,
        path_prefix: '/user',
    },
]

export const AuthRouter = [
    {
        path: '/login',
        name: 'Login',
        icon: '',
        component: LoginPage,
        path_prefix: '/session',
    },
    {
        path: '/logout',
        name: 'Logout',
        icon: '',
        component: LogoutPage,
        path_prefix: '/session',
    },
    {
        path: '/register',
        name: 'Register',
        icon: '',
        component: RegisterPage,
        path_prefix: '/session',
    },
    {
        path: '/confirm-account',
        name: 'ConfirmAccount',
        icon: '',
        component: RegisterValidatePage,
        path_prefix: '/session'
    },
    {
        path: '/forget-password',
        name: 'ApplyResetPassword',
        icon: '',
        component: ApplyResetPasswordPage,
        path_prefix: '/session',
    },
    {
        path: '/reset-password',
        name: 'ResetPassword',
        icon: '',
        component: ResetPasswordPage,
        path_prefix: '/session'
    }
]