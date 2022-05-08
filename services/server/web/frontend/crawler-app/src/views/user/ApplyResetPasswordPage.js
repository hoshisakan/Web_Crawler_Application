import React, { useState, useEffect } from 'react'
import { Form, Button, Row, Col, Card, Container, Alert } from 'react-bootstrap'
import { apiApplyResetPassword } from '../../api.js'

export default function ApplyResetPasswordPage(props) {
    const currentWindowSize = props.currentWindowSize === undefined ? '28rem' : props.currentWindowSize
    const [email, setEmail] = useState('')
    const [applySuccess, setApplySuccess] = useState(false)
    const [applyFailure, setApplyFailure] = useState(false)
    const [cardWidth, setCardWidth] = useState('28rem')

    const handleEmailChange = (e) => {
        setEmail(e.target.value)
    }

    const validateForm = () => {
        return email.length === 0
    }

    const handleApplySubmit = () => {
        let data = {
            email: email,
        }
        apiApplyResetPassword(data)
            .then((res) => {
                if (res.data['apply_reset_success']) {
                    setApplyFailure(false)
                    setApplySuccess(true)
                }
            })
            .catch((err) => {
                setApplyFailure(true)
                setApplySuccess(false)
            })
    }

    useEffect(() => {
        if (currentWindowSize.x < 1000) {
            setCardWidth('23rem')
        } else if (currentWindowSize.x >= 1000 && currentWindowSize.x <= 1600) {
            setCardWidth('27rem')
        } else if (currentWindowSize.x > 1600 && currentWindowSize.x < 1900) {
            setCardWidth('30rem')
        } else {
            setCardWidth('30rem')
        }
    }, [currentWindowSize])

    return (
        <Container>
            <Row>
                <Col md={12}>
                    <Card style={{ width: cardWidth }} border="light" bg="light" text="black" className="card-mt-1">
                        <Form>
                            <Card.Header>Apply Reset Password</Card.Header>
                            <Card.Body>
                                {applySuccess ? (
                                    <Alert variant="success">
                                        <Alert.Heading>Apply Success</Alert.Heading>
                                        <p className="mb-0">
                                            Please go to your mailbox to receive the reset password email
                                        </p>
                                    </Alert>
                                ) : null}
                                {applyFailure ? (
                                    <Alert variant="danger">
                                        <Alert.Heading>Apply Failed</Alert.Heading>
                                        <p className="mb-0">
                                            Please check field whether or enter duplicate username or email
                                        </p>
                                    </Alert>
                                ) : null}
                                <Form.Group controlId="formEmail" className="align-items-left-2">
                                    <Form.Label className="form-horizontal.control-label">Email</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Email"
                                        onChange={handleEmailChange}
                                        value={email}
                                    />
                                </Form.Group>
                            </Card.Body>
                            <Card.Footer>
                                <div className="d-grid gap-2">
                                    <Button
                                        variant="primary"
                                        size="sm"
                                        onClick={handleApplySubmit}
                                        disabled={validateForm()}
                                    >
                                        Apply Reset Password
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
