import React, { useState, useEffect } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { Form, Button, Row, Col, Card, Container } from 'react-bootstrap'
import { setToken } from '../../auth.js'
import { apiUserLogin } from '../../api.js'
import '../../assets/css/login_page_style.css'

export default function LoginPage(props) {
    const currentWindowSize = props.currentWindowSize === undefined ? 0 : props.currentWindowSize
    const history = useHistory()
    const [formInputArray, setFormInputArray] = useState([{ username: '', password: '' }])
    const [displayErrorMessage, setDisplayErrorMessage] = useState(false)
    const [errorMessage, setErrorMessage] = useState('')
    const [cardWidth, setCardWidth] = useState('28rem')
    const [cardBtnSpacing, setCardBtnSpacing] = useState('10.5rem')
    const [usernameErrorMsg, setUsernameErrorMsg] = useState('')
    const [passwordErrorMsg, setPasswordErrorMsg] = useState('')
    const [displayFieldErrorMsg, setDisplayFieldErrorMsg] = useState(false)

    const clearErrorRemindInfo = () => {
        setDisplayFieldErrorMsg(false)
        setErrorMessage('')
        setDisplayErrorMessage(false)
        setUsernameErrorMsg('')
        setPasswordErrorMsg('')
    }

    const handleLoginSubmit = (e) => {
        if (formInputArray[0].username.length > 0 && formInputArray[0].password.length > 0) {
            clearErrorRemindInfo()
            apiUserLogin(formInputArray[0])
                .then((res) => {
                    let access_token = res.data['access']
                    let refresh_token = res.data['refresh']
                    setToken(access_token, refresh_token)
                    setDisplayErrorMessage(false)
                    history.push('/user/ptt')
                })
                .catch((err) => {
                    setDisplayErrorMessage(true)
                    setErrorMessage('Login Failed')
                })
            setFormInputArray([{ username: '', password: '' }])
        } else if (formInputArray[0].username.length < 1 && formInputArray[0].password.length > 0) {
            setErrorMessage('')
            setDisplayErrorMessage(false)
            setDisplayFieldErrorMsg(true)
            setUsernameErrorMsg('The field is required')
            setPasswordErrorMsg('')
        } else if (formInputArray[0].username.length > 0 && formInputArray[0].password.length < 1) {
            setErrorMessage('')
            setDisplayErrorMessage(false)
            setDisplayFieldErrorMsg(true)
            setUsernameErrorMsg('')
            setPasswordErrorMsg('The field is required')
        } else {
            setErrorMessage('')
            setDisplayErrorMessage(false)
            setDisplayFieldErrorMsg(true)
            setUsernameErrorMsg('The field is required')
            setPasswordErrorMsg('The field is required')
        }
    }

    const handleFormInputArray = (e) => {
        const { name, value } = e.target
        const temp = [...formInputArray]
        temp[0][name] = value
        setFormInputArray(temp)
    }

    useEffect(() => {
        if (currentWindowSize.x < 1000) {
            setCardWidth('23rem')
            setCardBtnSpacing('5.0rem')
        } else if (currentWindowSize.x >= 1000 && currentWindowSize.x <= 1600) {
            setCardWidth('30rem')
            setCardBtnSpacing('11.5rem')
        } else {
            setCardWidth('30rem')
            setCardBtnSpacing('11.5rem')
        }
    }, [currentWindowSize])

    return (
        <Container>
            <Row>
                <Col md={12}>
                    <Card style={{ width: cardWidth }} border="light" bg="light" text="black" className="card-mt-1">
                        <Card.Header>User Login</Card.Header>
                        <Card.Body>
                            <Form.Group controlId="formUsrname" className="align-items-left-2">
                                <Form.Label className="form-horizontal.control-label">Usrename</Form.Label>
                                <Form.Control
                                    name="username"
                                    type="text"
                                    placeholder="Username"
                                    value={formInputArray[0].username}
                                    onChange={(e) => handleFormInputArray(e)}
                                />
                            </Form.Group>
                            {displayFieldErrorMsg ? <div className="field-error-remind">{usernameErrorMsg}</div> : null}
                            <br />
                            <Form.Group controlId="formPassword" className="align-items-left-2">
                                <Form.Label className="form-horizontal.control-label">Password</Form.Label>
                                <Form.Control
                                    name="password"
                                    type="password"
                                    placeholder="Password"
                                    value={formInputArray[0].password}
                                    onChange={(e) => handleFormInputArray(e)}
                                />
                            </Form.Group>
                            {displayFieldErrorMsg ? <div className="field-error-remind">{passwordErrorMsg}</div> : null}
                            {displayErrorMessage ? <div className="field-error-remind">{errorMessage}</div> : null}
                            <br />
                            <div className="d-grid gap-2">
                                <Button variant="primary" size="sm" onClick={handleLoginSubmit}>
                                    Login
                                </Button>
                            </div>
                        </Card.Body>
                        <Card.Footer>
                            <span style={{ textAlign: 'left', marginRight: cardBtnSpacing }}>
                                <Link to="/session/register">
                                    <Button variant="success">Register</Button>
                                </Link>
                            </span>

                            <span style={{ textAlign: 'right' }}>
                                <Link to="/session/forget-password">Forget your password?</Link>
                            </span>
                        </Card.Footer>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
}
