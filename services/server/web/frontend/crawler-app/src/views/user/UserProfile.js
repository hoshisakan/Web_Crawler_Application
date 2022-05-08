import React, { useState, useEffect } from 'react'
import { Form, Card, Container } from 'react-bootstrap'
import '../../assets/css/form_level_style.css'
import useInterval from '../../components/Timer/useInterval'
import { getCurrentWindowSize } from '../../assets/js/getWindowSize.js'

export default function UserProfile(props) {
    const { username, email } = props
    const [currentWindowSize, setCurrentWindowSize] = useState(getCurrentWindowSize())
    const [cardWidth, setCardWidth] = useState('28rem')

    useInterval(() => {
        setCurrentWindowSize(getCurrentWindowSize())
    }, 1000)

    useEffect(() => {
        if (currentWindowSize.x < 1000) {
            setCardWidth('22rem')
        } else if (currentWindowSize.x >= 1000) {
            setCardWidth('30rem')
        }
    }, [currentWindowSize])

    return (
        <Container fluid className="card-root">
            <Card
                style={{ width: cardWidth, height: '16rem' }}
                border="dark"
                bg="light"
                text="black"
                className="card-mt-1"
            >
                <Form>
                    <Card.Header>User Profile</Card.Header>

                    <Card.Body>
                        <Form.Group controlId="formUsrname" className="align-items-left-2">
                            <Form.Label className="form-horizontal.control-label">Usrename</Form.Label>
                            <Form.Control type="text" placeholder="Username" value={username} disabled />
                        </Form.Group>
                        <br />
                        <Form.Group controlId="formEmail" className="align-items-left-2">
                            <Form.Label className="form-horizontal.control-label">Email</Form.Label>
                            <Form.Control type="email" placeholder="Email" value={email} disabled />
                        </Form.Group>
                    </Card.Body>
                </Form>
            </Card>
        </Container>
    )
}
