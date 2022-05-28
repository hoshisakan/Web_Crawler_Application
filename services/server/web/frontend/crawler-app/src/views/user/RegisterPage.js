import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Form, Button, Row, Col, Card, Container, Alert } from 'react-bootstrap'
import '../../assets/css/form_level_style.css'
import '../../assets/css/register_page_style.css'
import { apiRegisterUser, apiReissueRegister } from '../../api.js'

export default function RegisterPage(props) {
    const currentWindowSize = props.currentWindowSize === undefined ? '' : props.currentWindowSize
    const [email, setEmail] = useState('')
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [rePassword, setRePassword] = useState('')
    const [showRegisterSuccess, setShowRegisterSuccess] = useState(false)
    const [registerMsg, setRegisterMsg] = useState(false)
    const [usernameFieldAlert, setUsernameFieldAlert] = useState('')
    const [emailFieldAlert, setEmailFieldAlert] = useState('')
    const [displayReissueMsg, setDisplayReissueMsg] = useState(false)
    const [reissueMsg, setReissueMsg] = useState('')
    const [cardWidth, setCardWidth] = useState('28rem')

    const handleUsernameChange = (e) => {
        setUsername(e.target.value)
    }

    const handleEmailChange = (e) => {
        setEmail(e.target.value)
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value)
    }

    const handleRePasswordChange = (e) => {
        setRePassword(e.target.value)
    }

    const checkSubmitValues = () => {
        return (
            username.length === 0 ||
            email.length === 0 ||
            password.length === 0 ||
            rePassword.length === 0 ||
            password !== rePassword
        )
    }

    const clearAlertMessage = () => {
        setUsernameFieldAlert('')
        setEmailFieldAlert('')
    }

    const handleRegisterSubmit = () => {
        clearAlertMessage()
        if (username === 'admin') {
            setUsernameFieldAlert(`The username 'admin' disable`)
        } else {
            let data = {
                username: username,
                email: email,
                password: password,
            }
            apiRegisterUser(data)
                .then((res) => {
                    let data = res.data
                    if (data['is_registered'] === true) {
                        setShowRegisterSuccess(true)
                        setRegisterMsg(data['message'])
                    }
                })
                .catch((err) => {
                    setShowRegisterSuccess(false)
                    let detail = err.response.data['error']
                    if (detail['is_username_registered'] === true && detail['is_email_registered'] === true) {
                        setUsernameFieldAlert('The username has been use')
                        setEmailFieldAlert('The email has been registerd')
                    } else if (detail['is_username_registered'] === true || detail['is_email_registered'] === true) {
                        detail['is_username_registered'] === true
                            ? setUsernameFieldAlert('The username has been use')
                            : setEmailFieldAlert('The email has been registerd')
                    }
                })
        }
    }

    const clearReissueMessage = () => {
        setReissueMsg('')
        setDisplayReissueMsg(false)
    }

    const handleReissueRequest = () => {
        clearReissueMessage()
        let data = {
            username: username,
            email: email,
        }
        apiReissueRegister(data)
            .then((res) => {
                let data = res.data
                if (res.status === 200 && data['is_reissue'] === true) {
                    setReissueMsg(data['message'])
                    setDisplayReissueMsg(true)
                    setShowRegisterSuccess(false)
                }
            })
            .catch((err) => {
                clearReissueMessage()
            })
    }

    useEffect(() => {
        if (currentWindowSize.x < 1000) {
            setCardWidth('23rem')
        } else if (currentWindowSize.x >= 1000 && currentWindowSize.x <= 1600) {
            setCardWidth('28rem')
        } else {
            setCardWidth('31rem')
        }
    }, [currentWindowSize])

    return (
        <Container fluid>
            <Row>
                <Col md={12}>
                    <Card style={{ width: cardWidth }} border="black" bg="light" text="black" className="card-mt-1">
                        <Form>
                            <Card.Header>User Register</Card.Header>

                            <Card.Body>
                                {showRegisterSuccess ? (
                                    <div>
                                        <Alert variant="success">
                                            <Alert.Heading>Register Successfully</Alert.Heading>
                                            <p>{registerMsg}</p>
                                            <hr />
                                            <div className="btn-mt-1">
                                                <Button variant="primary" onClick={handleReissueRequest}>
                                                    Didn't receive the verification email?
                                                </Button>
                                            </div>
                                        </Alert>
                                    </div>
                                ) : null}
                                {displayReissueMsg ? (
                                    <div>
                                        <Alert variant="success">
                                            <Alert.Heading>Reissue Successfully</Alert.Heading>
                                            <p>{reissueMsg}</p>
                                        </Alert>
                                    </div>
                                ) : null}
                                <Form.Group controlId="formUsrname" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">Usrename</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Username"
                                        onChange={handleUsernameChange}
                                        value={username}
                                    />
                                    <p className="field-alert">{usernameFieldAlert}</p>
                                </Form.Group>
                                <Form.Group controlId="formEmail" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">Email</Form.Label>
                                    <Form.Control
                                        type="email"
                                        placeholder="Email"
                                        onChange={handleEmailChange}
                                        value={email}
                                    />
                                    <p className="field-alert">{emailFieldAlert}</p>
                                </Form.Group>
                                <Form.Group controlId="formPassword" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Password"
                                        onChange={handlePasswordChange}
                                        value={password}
                                    />
                                </Form.Group>
                                <Form.Group controlId="formRePassword" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">Re-enter Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Re-Enter Password"
                                        onChange={handleRePasswordChange}
                                        value={rePassword}
                                    />
                                </Form.Group>
                                <br />
                                <div className="d-grid gap-2">
                                    <Button
                                        variant="primary"
                                        onClick={handleRegisterSubmit}
                                        disabled={checkSubmitValues()}
                                        size="sm"
                                    >
                                        Register
                                    </Button>
                                </div>
                            </Card.Body>
                            <Card.Footer>
                                <div style={{ textAlign: 'center' }}>
                                    Already have an account? <Link to="/session/login">Sign in</Link>
                                </div>
                            </Card.Footer>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
}
