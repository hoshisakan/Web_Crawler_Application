import React, { useState, useCallback, useEffect } from 'react'
import { Button, Container, Row, Col, Form, Toast, ToastContainer, Modal } from 'react-bootstrap'
import {
    viewPttInfoColumns,
    taskResultColumns,
    boardOptions,
    actionModeOptions,
    keywordModeOptions,
} from './dropdown_options'
import useInterval from '../../components/Timer/useInterval'
import TaskTableList from '../../components/Table/ptt/TaskTableList'
import { delay } from '../../components/Timer/delay'
import { apiObtainExtraTaskInfo, apiObtainPttInfo } from '../../api.js'
import ViewPttInfoTable from '../../components/Table/ptt/ViewPttInfoTable'

export default function Search(props) {
    const currentWindowSize = props.currentWindowSize === undefined ? 0 : props.currentWindowSize
    const [taskResultRows, setTaskResultRowData] = useState([])
    const [viewInfoResultRows, setviewInfoResultRows] = useState([])
    const [currentViewTaskId, setCurrentViewTaskId] = useState('')
    const [taskTableSize] = useState('lg')
    const [taskTableResponsive] = useState('sm')
    const [viewInfoTableSize] = useState('sm')
    const [viewInfoTableResponsive] = useState('sm')
    const [formInputArray, setFormInputArray] = useState([
        {
            action_mode: '',
            search_keyword: '',
            search_page_count: 0,
            search_page_limit_enable: '',
            board_name: '',
        },
    ])
    const [allowAddTask, setAllowAddTask] = useState(false)
    const [addTaskId, setAddTaskId] = useState('')
    const [displayAddTaskRemind, setDisplayAddTaskRemind] = useState(false)
    const [displayCheckNotPassRemind, setDisplayCheckNotPassRemind] = useState(false)
    const [displayViewTaskResult, setDisplayViewTaskResult] = useState(false)
    const [updateTaskProgressAllow, setUpdateTaskProgressAllow] = useState(true)
    const [disableSearchButton, setDisableSearchButton] = useState(false)
    const taskCreateRemindPosition =
        currentWindowSize.x > 1000 || currentWindowSize === undefined ? 'top-end' : 'top-center'
    const [showAddTaskModal, setShowAddTaskModal] = useState(false)

    const closeDisplayCheckNotPassRemind = () => {
        setDisplayCheckNotPassRemind(!displayCheckNotPassRemind)
    }

    const closeDisplayViewTaskResult = () => {
        setDisplayViewTaskResult(!displayViewTaskResult)
    }

    const handleCloseAddTaskModal = () => {
        setShowAddTaskModal(false)
        setFormInputArray([
            {
                action_mode: '',
                search_keyword: '',
                search_page_count: 0,
                search_page_limit_enable: '',
                board_name: '',
            },
        ])
        setAllowAddTask(false)
    }

    const handleFormInputArray = (e) => {
        const { name, value } = e.target
        const tempList = [...formInputArray]
        if (
            (name === 'search_page_count' || name === 'action_mode' || name === 'search_page_limit_enable') &&
            value === 'None'
        ) {
            if (name === 'search_page_limit_enable') {
                tempList[0]['search_page_count'] = 0
            }
            tempList[0][name] = ''
        } else if (name === 'action_mode' && value !== 'None') {
            tempList[0]['search_keyword'] = ''
            tempList[0]['board_name'] = ''
            tempList[0]['search_page_count'] = 0
            tempList[0][name] = value
        } else if (name === 'search_page_limit_enable' && value !== 'None') {
            const tempValue = JSON.parse(value)
            if (!tempValue) {
                tempList[0]['search_page_count'] = 0
            }
            tempList[0][name] = tempValue
        } else {
            tempList[0][name] = value
        }
        setFormInputArray(tempList)
    }

    const closeDisplayAddTaskRemind = () => {
        setDisplayAddTaskRemind(!displayAddTaskRemind)
    }

    const resetInputArrayState = () => {
        setFormInputArray([
            {
                action_mode: '',
                search_keyword: '',
                search_page_count: 0,
                search_page_limit_enable: '',
                board_name: '',
            },
        ])
        setAllowAddTask(false)
        setDisplayAddTaskRemind(false)
        setDisableSearchButton(true)
    }

    const addTask = async () => {
        let temp = [...formInputArray]
        resetInputArrayState()
        // console.log(JSON.stringify(temp[0]))
        await apiObtainPttInfo(temp[0])
            .then((res) => {
                let data = res.data
                // console.log(data)
                // alert(data)
                setAddTaskId(data['task_id'])
                setDisplayAddTaskRemind(true)
            })
            .catch((err) => {
                console.error(err.message)
                // alert(err.message)
            })
    }

    useInterval(() => {
        setUpdateTaskProgressAllow(true)
    }, 1000)

    const requestTaskProgress = useCallback(() => {
        const updateTaskProgress = async () => {
            if (updateTaskProgressAllow === true) {
                // console.log('updateTaskProgressAllow: ' + updateTaskProgressAllow)
                let query_params = {
                    data_source: 'ptt',
                }
                await apiObtainExtraTaskInfo(query_params)
                    .then((res) => {
                        let data = res.data
                        // console.log(data)
                        setTaskResultRowData(data)
                    })
                    .catch((err) => {
                        console.log(err.message)
                    })
                setUpdateTaskProgressAllow(false)
            }
        }
        const waitCloseAddTaskRemind = async () => {
            if (displayAddTaskRemind === true) {
                await delay(2000)
                setDisplayAddTaskRemind(!displayAddTaskRemind)
                setDisableSearchButton(false)
            }
        }
        updateTaskProgress()
        waitCloseAddTaskRemind()
    }, [displayAddTaskRemind, updateTaskProgressAllow])

    const handleSendSearch = () => {
        if (
            formInputArray[0].action_mode === 'Page' &&
            formInputArray[0].board_name.length > 0 &&
            formInputArray[0].search_page_count > 0
        ) {
            addTask()
        } else if (
            formInputArray[0].action_mode === 'Keyword' &&
            formInputArray[0].board_name.length > 0 &&
            formInputArray[0].search_keyword.length > 0 &&
            formInputArray[0].search_page_limit_enable &&
            formInputArray[0].search_page_count > 0
        ) {
            addTask()
        } else if (
            formInputArray[0].action_mode === 'Keyword' &&
            formInputArray[0].board_name.length > 0 &&
            formInputArray[0].search_keyword.length > 0 &&
            formInputArray[0].search_page_limit_enable === false
        ) {
            addTask()
        } else {
            setDisplayCheckNotPassRemind(true)
        }
    }

    const handleCancelAddTask = () => {
        setAllowAddTask(false)
        setFormInputArray([
            {
                action_mode: '',
                search_keyword: '',
                search_page_count: 0,
                search_page_limit_enable: '',
                board_name: '',
            },
        ])
    }

    const handleAddTaskClick = () => {
        setAllowAddTask(true)
        if (currentWindowSize.x <= 1000) {
            setShowAddTaskModal(true)
        }
    }

    useEffect(() => {
        requestTaskProgress()
    }, [requestTaskProgress])

    return (
        <Container fluid>
            <br />
            {allowAddTask === true ? null : (
                <Row>
                    <Col>
                        <Button
                            variant="danger"
                            id="add_task_button"
                            disabled={disableSearchButton}
                            onClick={handleAddTaskClick}
                        >
                            Add Task
                        </Button>
                    </Col>
                </Row>
            )}
            {allowAddTask === true ? (
                currentWindowSize.x > 1000 ? (
                    <Row>
                        <Col xs="auto">
                            <Form.Select
                                name="action_mode"
                                placeholder="Select Action Mode"
                                disabled={disableSearchButton}
                                value={formInputArray[0].action_mode}
                                onChange={(e) => handleFormInputArray(e)}
                            >
                                {actionModeOptions.map((action_mode) => {
                                    return (
                                        <option key={action_mode.id} value={action_mode.value}>
                                            {action_mode.id}
                                        </option>
                                    )
                                })}
                            </Form.Select>
                        </Col>
                        {formInputArray[0].action_mode === 'Keyword' ? (
                            <Col xs="auto">
                                <Form.Select
                                    name="search_page_limit_enable"
                                    placeholder="Select Enable Page Search"
                                    disabled={disableSearchButton}
                                    value={formInputArray[0].search_page_limit_enable}
                                    onChange={(e) => handleFormInputArray(e)}
                                >
                                    {keywordModeOptions.map((keyword_mode) => {
                                        return (
                                            <option key={keyword_mode.id} value={keyword_mode.value}>
                                                {keyword_mode.id}
                                            </option>
                                        )
                                    })}
                                </Form.Select>
                            </Col>
                        ) : null}
                        {(formInputArray[0].search_page_limit_enable && formInputArray[0].action_mode === 'Keyword') ||
                        formInputArray[0].action_mode === 'Page' ? (
                            <Col xs="auto">
                                <Form.Control
                                    type="number"
                                    name="search_page_count"
                                    disabled={disableSearchButton}
                                    value={formInputArray[0].search_page_count}
                                    onChange={(e) => handleFormInputArray(e)}
                                ></Form.Control>
                            </Col>
                        ) : null}
                        {formInputArray[0].action_mode === 'Page' || formInputArray[0].action_mode === 'Keyword' ? (
                            <Col xs="auto">
                                <Form.Select
                                    name="board_name"
                                    disabled={disableSearchButton}
                                    value={formInputArray[0].board_name}
                                    onChange={(e) => handleFormInputArray(e)}
                                >
                                    {boardOptions.map((board_option) => {
                                        return (
                                            <option key={board_option.id} value={board_option.value}>
                                                {board_option.id}
                                            </option>
                                        )
                                    })}
                                </Form.Select>
                            </Col>
                        ) : null}
                        {formInputArray[0].action_mode === 'Keyword' ? (
                            <Col xs="3">
                                <Form.Control
                                    type="text"
                                    placeholder="Enter Keyword"
                                    name="search_keyword"
                                    onChange={(e) => handleFormInputArray(e)}
                                    value={formInputArray[0].search_keyword}
                                    disabled={disableSearchButton}
                                />
                            </Col>
                        ) : null}
                        <Col xs="auto">
                            <Button
                                style={{ marginRight: '0.65rem' }}
                                variant="primary"
                                id="search-button"
                                onClick={handleSendSearch}
                                disabled={disableSearchButton}
                            >
                                Search
                            </Button>
                            <Button
                                variant="danger"
                                id="cancel-button"
                                onClick={handleCancelAddTask}
                                disabled={disableSearchButton}
                            >
                                Cancel
                            </Button>
                        </Col>
                    </Row>
                ) : (
                    <Modal show={showAddTaskModal} onHide={handleCloseAddTaskModal}>
                        <Modal.Header closeButton>
                            <Modal.Title>Add task</Modal.Title>
                        </Modal.Header>

                        <Modal.Body>
                            <Form.Group className="mb-3" controlId="formBasicActionMode">
                                <Form.Label>Search Action Mode</Form.Label>
                                <Form.Select
                                    name="action_mode"
                                    placeholder="Select Action Mode"
                                    disabled={disableSearchButton}
                                    value={formInputArray[0].action_mode}
                                    onChange={(e) => handleFormInputArray(e)}
                                >
                                    {actionModeOptions.map((action_mode) => {
                                        return (
                                            <option key={action_mode.id} value={action_mode.value}>
                                                {action_mode.id}
                                            </option>
                                        )
                                    })}
                                </Form.Select>
                            </Form.Group>
                            {formInputArray[0].action_mode === 'Keyword' ? (
                                <Form.Group className="mb-3" controlId="formBasiEnablePageSearch">
                                    <Form.Label>Enable Page Search</Form.Label>
                                    <Form.Select
                                        name="search_page_limit_enable"
                                        placeholder="Select Enable Page Search"
                                        disabled={disableSearchButton}
                                        value={formInputArray[0].search_page_limit_enable}
                                        onChange={(e) => handleFormInputArray(e)}
                                    >
                                        {keywordModeOptions.map((keyword_mode) => {
                                            return (
                                                <option key={keyword_mode.id} value={keyword_mode.value}>
                                                    {keyword_mode.id}
                                                </option>
                                            )
                                        })}
                                    </Form.Select>
                                </Form.Group>
                            ) : null}
                            {(formInputArray[0].search_page_limit_enable &&
                                formInputArray[0].action_mode === 'Keyword') ||
                            formInputArray[0].action_mode === 'Page' ? (
                                <Form.Group className="mb-3" controlId="formBasiPageCount">
                                    <Form.Label>Search Page Count</Form.Label>
                                    <Form.Control
                                        type="number"
                                        name="search_page_count"
                                        disabled={disableSearchButton}
                                        value={formInputArray[0].search_page_count}
                                        onChange={(e) => handleFormInputArray(e)}
                                    ></Form.Control>
                                </Form.Group>
                            ) : null}
                            {formInputArray[0].action_mode === 'Page' || formInputArray[0].action_mode === 'Keyword' ? (
                                <Form.Group className="mb-3" controlId="formBasiPttBoardName">
                                    <Form.Label>Ptt Board Name</Form.Label>
                                    <Form.Select
                                        name="board_name"
                                        disabled={disableSearchButton}
                                        value={formInputArray[0].board_name}
                                        onChange={(e) => handleFormInputArray(e)}
                                    >
                                        {boardOptions.map((board_option) => {
                                            return (
                                                <option key={board_option.id} value={board_option.value}>
                                                    {board_option.id}
                                                </option>
                                            )
                                        })}
                                    </Form.Select>
                                </Form.Group>
                            ) : null}
                            {formInputArray[0].action_mode === 'Keyword' ? (
                                <Form.Group className="mb-3" controlId="formBasicKeyword">
                                    <Form.Label>Search keyword</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter Keyword"
                                        name="search_keyword"
                                        onChange={(e) => handleFormInputArray(e)}
                                        value={formInputArray[0].search_keyword}
                                        disabled={disableSearchButton}
                                    />
                                </Form.Group>
                            ) : null}
                        </Modal.Body>

                        <Modal.Footer>
                            <Button
                                variant="primary"
                                id="search-button"
                                onClick={handleSendSearch}
                                disabled={disableSearchButton}
                            >
                                Search
                            </Button>
                            <Button variant="danger" onClick={handleCloseAddTaskModal}>
                                Cancel
                            </Button>
                        </Modal.Footer>
                    </Modal>
                )
            ) : null}
            <Row>
                <Col xs="auto">
                    <ToastContainer position={taskCreateRemindPosition} className="p-3">
                        <Toast
                            bg={'Primary'.toLowerCase()}
                            show={displayAddTaskRemind}
                            onClose={closeDisplayAddTaskRemind}
                        >
                            <Toast.Header className={'text-black'}>
                                <strong className="me-auto">Create task success</strong>
                                <small className="text-muted">just now</small>
                            </Toast.Header>
                            <Toast.Body className={'text-white'}>task id: {addTaskId}</Toast.Body>
                        </Toast>
                    </ToastContainer>
                </Col>
            </Row>
            <br />
            <Row>
                <Modal show={displayViewTaskResult} onHide={closeDisplayViewTaskResult} fullscreen={true}>
                    <Modal.Header closeButton>
                        <Modal.Title>{currentViewTaskId}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <ViewPttInfoTable
                            viewInfoTableRows={viewInfoResultRows}
                            viewInfoTableCols={viewPttInfoColumns}
                            viewInfoTableSize={viewInfoTableSize}
                            viewInfoTableResponsive={viewInfoTableResponsive}
                        />
                    </Modal.Body>
                </Modal>
            </Row>
            <Row>
                <Modal show={displayCheckNotPassRemind} onHide={closeDisplayCheckNotPassRemind}>
                    <Modal.Header closeButton>
                        <Modal.Title>Send Request Failed</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Input can't be empty</Modal.Body>
                    <Modal.Footer>
                        <Button variant="danger" onClick={closeDisplayCheckNotPassRemind}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
            </Row>
            <Row>
                <TaskTableList
                    taskTableRows={taskResultRows}
                    taskTableCols={taskResultColumns}
                    taskTableSize={taskTableSize}
                    taskTableResponsive={taskTableResponsive}
                    callBackViewTaskResultRows={setviewInfoResultRows}
                    callBackCurrentViewTaskId={setCurrentViewTaskId}
                    callBackDisplayViewTaskResult={setDisplayViewTaskResult}
                />
            </Row>
        </Container>
    )
}
