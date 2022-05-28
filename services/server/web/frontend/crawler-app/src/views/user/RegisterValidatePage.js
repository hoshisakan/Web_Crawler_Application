import React, { useState, useCallback, useEffect } from 'react'
import { useHistory, useLocation } from 'react-router-dom'
import { Button, Row, Container, Alert } from 'react-bootstrap'
import { apiRegisterValidate } from '../../api.js'
import useInterval from '../../components/Timer/useInterval'
import '../../assets/css/register_page_style.css'

export default function RegisterValidatePage() {
    const history = useHistory()
    const { search } = useLocation()
    const searchParams = new URLSearchParams(search)
    const token = searchParams.get('token')
    const [showJumpLoginModal, setJumpLoginModal] = useState(false)
    const [delay] = useState(1000)
    const [countdown, setCountdown] = useState(5)
    const [validateFailure, setValidateFailure] = useState(false)
    const [failureAlertMsg, setFailureAlertMsg] = useState('')

    useInterval(
        () => {
            countdown === 0 ? history.push('/session/login') : setCountdown(countdown - 1)
        },
        showJumpLoginModal ? delay : null
    )

    const handleLoginRedirect = () => {
        history.push('/session/login')
    }

    const checkToken = useCallback(() => {
        setFailureAlertMsg('')
        const validateRegisterToken = async () => {
            let data = {
                token: token,
            }
            apiRegisterValidate(data)
                .then((res) => {
                    if (res.data['is_account_validated'] === true && res.status === 200) {
                        setJumpLoginModal(true)
                        setValidateFailure(false)
                    } else {
                        setJumpLoginModal(false)
                        setValidateFailure(true)
                    }
                })
                .catch((err) => {
                    setJumpLoginModal(false)
                    setValidateFailure(true)
                    setFailureAlertMsg(err.response.data.error)
                })
        }
        validateRegisterToken()
    }, [token])

    useEffect(() => {
        checkToken()
    }, [checkToken])

    return (
        <Container fluid>
            <Row>
                {showJumpLoginModal ? (
                    <div>
                        <Alert show={true} variant="success">
                            <Alert.Heading>Register Account Activated Successfully</Alert.Heading>
                            <div className="alert-text-1">
                                <p>Will be jump to sign page: {countdown}</p>
                            </div>
                            <hr />
                            <div className="d-flex justify-content-end">
                                <Button variant="primary" onClick={handleLoginRedirect}>
                                    Sign in now
                                </Button>
                            </div>
                        </Alert>
                    </div>
                ) : null}
            </Row>
            <Row>
                {validateFailure ? (
                    <Alert variant="danger">
                        <Alert.Heading>Validate User Account Failed</Alert.Heading>
                        <div className="alert-text-1">
                            <p>{failureAlertMsg}</p>
                        </div>
                        <hr />
                        <div className="d-flex justify-content-end">
                            <Button variant="danger" onClick={handleLoginRedirect}>
                                Return login page
                            </Button>
                        </div>
                    </Alert>
                ) : null}
            </Row>
        </Container>
    )
}
