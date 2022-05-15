import React, { useState, useEffect } from 'react'
import { useLocation, Link } from 'react-router-dom'
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap'
import { UserRouter } from '../../route/routes.js'

export default function UserHeader(props) {
    const location = useLocation()
    const getBrandText = () => {
        for (let i = 0; i < UserRouter.length; i++) {
            if (location.pathname.indexOf(UserRouter[i].path_prefix + UserRouter[i].path) !== -1) {
                return UserRouter[i].name
            }
        }
    }
    const username = props.username === undefined ? null : props.username
    const currentWindowSize = props.currentWindowSize === undefined ? null : props.currentWindowSize
    const [navExpanded, setNavExpanded] = useState(false)
    const [navComponentWidth, setNavComponentWidth] = useState('85%')

    const updateNavExpanded = (expanded) => {
        setNavExpanded(expanded)
    }

    const closeNavExpanded = () => {
        setNavExpanded(false)
    }

    const updateNavComponentWidth = () => {
        if (currentWindowSize.x >= 1000 && currentWindowSize.x <= 1600) {
            setNavComponentWidth('85%')
        } else if (currentWindowSize.x > 1600) {
            setNavComponentWidth('89%')
        }
    }

    useEffect(() => {
        updateNavComponentWidth()
    })

    return (
        <Navbar
            bg="dark"
            variant="dark"
            expand="lg"
            onToggle={updateNavExpanded}
            expanded={navExpanded}
            collapseOnSelect
        >
            <Container fluid>
                <Navbar.Brand>{getBrandText()}</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto" style={{ width: navComponentWidth }} onSelect={closeNavExpanded}>
                        <NavDropdown title="Guide" id="basic-nav-dropdown">
                            <NavDropdown.Item eventKey="5" as={Link} to="/user/google-search">
                                Google 搜尋資訊
                            </NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item eventKey="6" as={Link} to="/user/stock">
                                股票資訊搜尋
                            </NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item eventKey="7" as={Link} to="/user/ptt">
                                Ptt 文章搜尋
                            </NavDropdown.Item>
                        </NavDropdown>
                        <NavDropdown title="User" id="basic-nav-dropdown">
                            <NavDropdown.Item eventKey="9" as={Link} to="/user/profile">
                                Profile
                            </NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item eventKey="10" as={Link} to="/session/logout">
                                Logout
                            </NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    <Nav.Item className="ml-auto">
                        <Navbar.Text style={{ color: 'white', fontSize: '18px' }}>
                            Signed in as: <span style={{ fontWeight: 'bold' }}>{username}</span>
                        </Navbar.Text>
                    </Nav.Item>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}
