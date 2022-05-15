import React, { useState, useCallback, useEffect } from 'react'
import { Button, Container, Row, Col, Form, Toast, ToastContainer, Modal } from 'react-bootstrap'
import {
    viewNewsInfoColumns,
    viewVideoInfoColumns,
    taskResultColumns,
    dataTypeOptions,
} from './dropdown_options'
import '../../assets/css/views_page_style.css'
import { apiObtainExtraTaskInfo, apiObtainGoogleSearchInfo } from '../../api.js'
import useInterval from '../../components/Timer/useInterval'
import TaskTableList from '../../components/Table/google_search/TaskTableList'
import ViewNewsInfoTable from '../../components/Table/google_search/ViewNewsInfoTable'
import ViewVideoInfoTable from '../../components/Table/google_search/ViewVideoInfoTable'
import { delay } from '../../components/Timer/delay'

export default function Search(props) {
    const currentWindowSize = props.currentWindowSize === undefined ? 0 : props.currentWindowSize
    const [taskResultRows, setTaskResultRowData] = useState([])
    const [viewInfoResultRows, setviewInfoResultRows] = useState([])
    const [currentViewTaskId, setCurrentViewTaskId] = useState('')
    const [currentViewDataType, setCurrentViewDataType] = useState('')
    const [taskTableSize] = useState('lg')
    const [taskTableResponsive] = useState('sm')
    const [viewInfoTableSize] = useState('sm')
    const [viewInfoTableResponsive] = useState('sm')
    const [formInputArray, setFormInputArray] = useState([
        {
            search_keyword: '',
            search_page_count: 0,
            data_type: '',
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
                search_keyword: '',
                search_page_count: 0,
                data_type: '',
            },
        ])
        setAllowAddTask(false)
    }

    const handleFormInputArray = (e) => {
        const { name, value } = e.target
        // console.log(name, value)
        const tempList = [...formInputArray]
        if (name === 'data_type' && value === 'None') {
            tempList[0][name] = ''
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
                search_keyword: '',
                page_count: 0,
                data_type: '',
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
        await apiObtainGoogleSearchInfo(temp[0])
            .then((res) => {
                let data = res.data
                // console.log(data)
                setAddTaskId(data['task_id'])
                setDisplayAddTaskRemind(true)
            })
            .catch((err) => {
                console.error(err.message)
            })
    }

    const viewInfoTableList = () => {
        // console.log(currentViewDataType)
        if (currentViewDataType === 'google news') {
            return (
                <ViewNewsInfoTable
                    viewInfoTableRows={viewInfoResultRows}
                    viewInfoTableCols={viewNewsInfoColumns}
                    viewInfoTableSize={viewInfoTableSize}
                    viewInfoTableResponsive={viewInfoTableResponsive}
                />
            )
        } else if (currentViewDataType === 'google video') {
            return (
                <ViewVideoInfoTable
                    viewInfoTableRows={viewInfoResultRows}
                    viewInfoTableCols={viewVideoInfoColumns}
                    viewInfoTableSize={viewInfoTableSize}
                    viewInfoTableResponsive={viewInfoTableResponsive}
                />
            )
        }
    }

    useInterval(() => {
        setUpdateTaskProgressAllow(true)
    }, 1000)

    const requestTaskProgress = useCallback(() => {
        const updateTaskProgress = async () => {
            if (updateTaskProgressAllow === true) {
                // console.log('updateTaskProgressAllow: ' + updateTaskProgressAllow)
                let query_params = {
                    data_source: 'google search',
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
            formInputArray[0].search_keyword.length > 0 &&
            (formInputArray[0].search_page_count > 0) & (formInputArray[0].data_type.length > 0)
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
                search_keyword: '',
                search_page_count: 0,
                data_type: '',
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
                        <Col xs="auto">
                            <Form.Control
                                type="number"
                                name="search_page_count"
                                disabled={disableSearchButton}
                                value={formInputArray[0].search_page_count}
                                onChange={(e) => handleFormInputArray(e)}
                            />
                        </Col>
                        <Col xs="auto">
                            <Form.Select
                                name="data_type"
                                disabled={disableSearchButton}
                                value={formInputArray[0].data_type}
                                onChange={(e) => handleFormInputArray(e)}
                            >
                                {dataTypeOptions.map((data_type) => {
                                    return (
                                        <option key={data_type.id} value={data_type.value}>
                                            {data_type.value}
                                        </option>
                                    )
                                })}
                            </Form.Select>
                        </Col>
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
                            <br />
                            <Form.Group className="mb-3" controlId="formBasiPageCount">
                                <Form.Label>Search Page Count</Form.Label>
                                <Form.Control
                                    type="number"
                                    name="search_page_count"
                                    disabled={disableSearchButton}
                                    value={formInputArray[0].search_page_count}
                                    onChange={(e) => handleFormInputArray(e)}
                                />
                            </Form.Group>
                            <br />
                            <Form.Group className="mb-3" controlId="formBasiDataType">
                                <Form.Label>Search Data Type</Form.Label>
                                <Form.Select
                                    name="data_type"
                                    disabled={disableSearchButton}
                                    value={formInputArray[0].data_type}
                                    onChange={(e) => handleFormInputArray(e)}
                                >
                                    {dataTypeOptions.map((data_type) => {
                                        return (
                                            <option key={data_type.id} value={data_type.value}>
                                                {data_type.value}
                                            </option>
                                        )
                                    })}
                                </Form.Select>
                            </Form.Group>
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
                        <div>{viewInfoTableList()}</div>
                    </Modal.Body>
                    {/* <Modal.Footer>
                        <Button variant="danger" onClick={closeDisplayViewTaskResult}>
                            Close
                        </Button>
                    </Modal.Footer> */}
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
                    callBackCurrentViewDataType={setCurrentViewDataType}
                    // callBackUpdateTaskProgress={setUpdateTaskProgressAllow}
                />
            </Row>
        </Container>
    )
}
