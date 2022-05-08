import React, { useState, useEffect } from 'react'
import { useHistory, useLocation } from 'react-router-dom'
import { Form, Button, Row, Col, Card, Container, Alert, Modal } from 'react-bootstrap'
import '../../assets/css/form_level_style.css'
import { apiResetPassword } from '../../api.js'
import useInterval from '../../components/Timer/useInterval'

export default function RegisterPage(props) {
    const currentWindowSize = props.currentWindowSize === undefined ? '28rem' : props.currentWindowSize
    const history = useHistory()
    const { search } = useLocation()
    const searchParams = new URLSearchParams(search)
    const token = searchParams.get('token')
    const [newPassword, setNewPassword] = useState('')
    const [reNewPassword, setReNewPassword] = useState('')
    const [resetFailure, setResetFailure] = useState(false)
    const [showJumpLoginModal, setJumpLoginModal] = useState(false)
    const [delay] = useState(1000)
    const [countdown, setCountdown] = useState(5)
    const [errorMsg, setErrorMsg] = useState('')
    const [cardWidth, setCardWidth] = useState('28rem')

    const handlePasswordChange = (e) => {
        setNewPassword(e.target.value)
    }

    const handleRePasswordChange = (e) => {
        setReNewPassword(e.target.value)
    }

    const checkSubmitValues = () => {
        return newPassword.length === 0 || reNewPassword.length === 0 || newPassword !== reNewPassword
    }

    useInterval(
        () => {
            countdown === 0 ? history.push('/session/login') : setCountdown(countdown - 1)
        },
        showJumpLoginModal ? delay : null
    )

    const handleResetPasswordSubmit = () => {
        let data = {
            token: token,
            new_password: newPassword,
        }
        apiResetPassword(data)
            .then((res) => {
                if (res.status === 200 && res.data['is_password_changed']) {
                    setResetFailure(false)
                    setJumpLoginModal(true)
                } else {
                    setResetFailure(true)
                    setJumpLoginModal(false)
                }
            })
            .catch((err) => {
                setResetFailure(true)
                setJumpLoginModal(false)
                setErrorMsg(err.response.data.error)
            })
    }

    const handleLoginRedirect = () => {
        history.push('/session/login')
    }

    useEffect(() => {
        if (currentWindowSize.x < 1000) {
            setCardWidth('22rem')
        } else if (currentWindowSize.x >= 1000) {
            setCardWidth('30rem')
        }
    }, [currentWindowSize])

    return (
        <Container fluid>
            {showJumpLoginModal ? (
                <div>
                    <Modal show={showJumpLoginModal} backdrop="static" keyboard={false}>
                        <Modal.Header>
                            <Modal.Title>Reset Password Successfully</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Will be jump to sign page: {countdown}</Modal.Body>
                        <Modal.Footer>
                            <Button variant="primary" onClick={handleLoginRedirect}>
                                Sign in now
                            </Button>
                        </Modal.Footer>
                    </Modal>
                </div>
            ) : null}
            <Row>
                <Col md={12}>
                    <Card style={{ width: cardWidth }} border="black" bg="light" text="black" className="card-mt-1">
                        <Form>
                            <Card.Header>Reset Password</Card.Header>
                            <Card.Body>
                                {resetFailure ? (
                                    <Alert variant="danger">
                                        <Alert.Heading>Reset Password Failed</Alert.Heading>
                                        <p className="mb-0">{errorMsg}</p>
                                    </Alert>
                                ) : null}
                                <Form.Group controlId="formPassword" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">New Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="New Password"
                                        onChange={handlePasswordChange}
                                        value={newPassword}
                                    />
                                </Form.Group>
                                <Form.Group controlId="formRePassword" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">
                                        Re-enter New Password
                                    </Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Re-Enter New Password"
                                        onChange={handleRePasswordChange}
                                        value={reNewPassword}
                                    />
                                </Form.Group>
                            </Card.Body>

                            <Card.Footer>
                                <div className="link-mt-1">
                                    <Button
                                        variant="primary"
                                        block
                                        onClick={handleResetPasswordSubmit}
                                        disabled={checkSubmitValues()}
                                    >
                                        Reset Password
                                    </Button>
                                </div>
                            </Card.Footer>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
}
