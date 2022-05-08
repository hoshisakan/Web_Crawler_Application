import React from 'react'
// import { Container, Navbar, Nav, Row, Col } from 'react-bootstrap'
import { Container } from 'react-bootstrap'

const style = {
    backgroundColor: 'green',
    borderTop: '1px solid #E7E7E7',
    textAlign: 'center',
    padding: '20px',
    position: 'fixed',
    left: '0',
    bottom: '0',
    height: '6%',
    width: '100%',
}

export default function UserFooter() {
    return (
        <footer style={style}>
            <Container fluid>
                <p className="copyright text-center">
                    © {new Date().getFullYear()} Todolist website, For record book todo
                </p>
            </Container>
        </footer>
    )
}
