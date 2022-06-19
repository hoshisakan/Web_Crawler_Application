import React, { useState, useCallback, useEffect } from 'react'
import { Button, Container, Row, Col, Form, Toast, ToastContainer, Modal } from 'react-bootstrap'
import { countryOption, taskResultColumns, viewStockInfoColumns } from './dropdown_options'
import useInterval from '../../components/Timer/useInterval'
import { apiObtainExtraTaskInfo, apiObtainStockInfo } from '../../api.js'
import '../../assets/css/views_page_style.css'
import ViewDailyPriceTable from '../../components/Table/stock/ViewDailyPriceTable'
import TaskTableList from '../../components/Table/stock/TaskTableList'
import { delay } from '../../components/Timer/delay'
import GoogleChart from '../../components/Chart/GoogleChart.js'

export default function Search(props) {
    const [currentWindowSize, setCurrentWindowSize] = useState(props.currentWindowSize === undefined ? 0 : props.currentWindowSize)
    const [taskResultRows, setTaskResultRowData] = useState([])
    const [viewInfoRows, setviewInfoContentRows] = useState([])
    const [currentViewTaskId, setCurrentSelectedTaskId] = useState('')
    const [taskTableSize] = useState('lg')
    const [taskTableResponsive] = useState('sm')
    const [viewInfoTableSize] = useState('lg')
    const [viewInfoTableResponsive] = useState('sm')
    const [addTaskId, setAddTaskId] = useState('')
    const [displayAddTaskRemind, setDisplayAddTaskRemind] = useState(false)
    const [displayCheckNotPassRemind, setDisplayCheckNotPassRemind] = useState(false)
    const [displayViewTaskContent, setDisplayViewTaskContent] = useState(false)
    const [updateTaskProgressAllow, setUpdateTaskProgressAllow] = useState(true)
    const [disableSearchButton, setDisableSearchButton] = useState(false)
    const [chartRows, setChartRows] = useState([])
    const [displayChart, setDisplayChart] = useState(false)
    const [analysisType, setAnalysisType] = useState('')
    const chartHAxisTitle = 'Trade Date'
    const chartVAxisTitle = analysisType === 'All' ? 'Price' : analysisType
    const chartType = analysisType === 'All' ? 'LineChart' : 'AreaChart'
    const [formInputArray, setFormInputArray] = useState([
        {
            ticker: '',
            start_date: '',
            end_date: '',
            country: '',
        },
    ])
    const [allowAddTask, setAllowAddTask] = useState(false)
    const [mobileInputCurrentIndex, setMobileInputCurrentIndex] = useState(0)
    const [showAddTaskModal, setShowAddTaskModal] = useState(false)
    const [showNextTaskBtn, setShowNextTaskBtn] = useState(false)

    const taskCreateRemindPosition =
        currentWindowSize.x > 1000 || currentWindowSize === undefined ? 'top-end' : 'top-center'

    const handleMobileCloseAddTaskModal = () => {
        setShowAddTaskModal(false)
        setFormInputArray([
            {
                ticker: '',
                start_date: '',
                end_date: '',
                country: '',
            },
        ])
        setMobileInputCurrentIndex(0)
        setAllowAddTask(false)
        setShowNextTaskBtn(false)
    }

    const closeDisplayCheckNotPassRemind = () => {
        setDisplayCheckNotPassRemind(!displayCheckNotPassRemind)
    }

    const closeDisplayViewTaskResult = () => {
        setDisplayViewTaskContent(!displayViewTaskContent)
    }

    const closeDisplayChart = () => {
        setDisplayChart(!displayChart)
    }

    const handleFormInputArray = (e, index) => {
        let { name, value } = e.target
        let tempList = [...formInputArray]
        if (name === 'country' && value === 'None') {
            tempList[index][name] = ''
        } else {
            tempList[index][name] = value
        }
        setFormInputArray(tempList)
    }

    // handle click event of the Remove button
    const handleRemoveClick = (index) => {
        let list = [...formInputArray]
        list.splice(index, 1)
        setFormInputArray(list)
        if (formInputArray.length === 1) {
            setAllowAddTask(false)
            setFormInputArray([
                {
                    ticker: '',
                    start_date: '',
                    end_date: '',
                    country: '',
                },
            ])
        }
    }

    // handle mobile click event of the Add button
    const handleAddClick = () => {
        setFormInputArray([...formInputArray, { ticker: '', start_date: '', end_date: '', country: '' }])
    }

    // handle mobile click event of the Remove button
    const handleMobileRemoveClick = () => {
        let list = [...formInputArray]
        list.splice(mobileInputCurrentIndex, 1)
        setFormInputArray(list)
        if (list.length === 1) {
            setShowNextTaskBtn(false)
        }
        let tempCurrentIndex = mobileInputCurrentIndex - 1
        setMobileInputCurrentIndex(tempCurrentIndex)
    }

    // handle click event of the Add button
    const handleMobileAddClick = () => {
        setFormInputArray([...formInputArray, { ticker: '', start_date: '', end_date: '', country: '' }])
        // console.log(formInputArray.length)
        let tempCurrentIndex = mobileInputCurrentIndex + 1
        setMobileInputCurrentIndex(tempCurrentIndex)
        setShowNextTaskBtn(true)
    }

    const handleMobileGobackClick = () => {
        let tempCurrentIndex = mobileInputCurrentIndex - 1
        setMobileInputCurrentIndex(tempCurrentIndex)
    }

    const handleMobileNextClick = () => {
        let tempCurrentIndex = mobileInputCurrentIndex + 1
        setMobileInputCurrentIndex(tempCurrentIndex)
    }

    const closeDisplayAddTaskRemind = () => {
        setDisplayAddTaskRemind(!displayAddTaskRemind)
    }

    const addTask = async () => {
        setDisplayAddTaskRemind(false)
        setDisableSearchButton(true)
        handleMobileCloseAddTaskModal()
        let temp = [...formInputArray]

        await apiObtainStockInfo(temp)
            .then((res) => {
                let data = res.data
                setAddTaskId(data['task_id'])
                // console.log('data: ' + data)
                setDisplayAddTaskRemind(true)
            })
            .catch((err) => {
                console.log('error: ' + err.message)
                setDisableSearchButton(false)
            })
    }

    const viewInfoTableList = () => {
        return (
            <ViewDailyPriceTable
                viewInfoTableRows={viewInfoRows}
                viewInfoTableCols={viewStockInfoColumns}
                viewInfoTableSize={viewInfoTableSize}
                viewInfoTableResponsive={viewInfoTableResponsive}
            />
        )
    }

    const viewInfoChart = () => {
        let chart_info = null
        if (currentWindowSize.x > 1000 && currentWindowSize.x <= 1600) {
            chart_info = (
                <GoogleChart
                    data={chartRows}
                    width="100%"
                    height="700px"
                    hAxisTitle={chartHAxisTitle}
                    vAxisTitle={chartVAxisTitle}
                    chartType={chartType}
                />
            )
        } else if (currentWindowSize.x > 1600) {
            chart_info = (
                <GoogleChart
                    data={chartRows}
                    width="100%"
                    height="900px"
                    hAxisTitle={chartHAxisTitle}
                    vAxisTitle={chartVAxisTitle}
                    chartType={chartType}
                />
            )
        } else if (currentWindowSize.x <= 1000) {
            chart_info = (
                <GoogleChart
                    data={chartRows}
                    width="600px"
                    height="500px"
                    hAxisTitle={chartHAxisTitle}
                    vAxisTitle={chartVAxisTitle}
                    chartType={chartType}
                />
            )
        }
        return chart_info
    }

    const allowActionAdd = (index) => {
        let btn_col = null
        if (formInputArray.length === 5) {
            btn_col = (
                <Button variant="secondary" id="add-button" onClick={handleAddClick} disabled={true}>
                    Add
                </Button>
            )
        } else {
            btn_col = (
                <Button variant="secondary" id="add-button" onClick={handleAddClick} disabled={false}>
                    Add
                </Button>
            )
        }
        return btn_col
    }

    useInterval(() => {
        setUpdateTaskProgressAllow(true)
    }, 1000)

    const requestTaskProgress = useCallback(() => {
        const updateTaskProgress = async () => {
            if (updateTaskProgressAllow === true) {
                let query_params = {
                    data_source: 'yahoo finance',
                    data_type: 'stock',
                }
                // console.log('updateTaskProgressAllow: ' + updateTaskProgressAllow)
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
        let check_result = true
        for (let i = 0; i < formInputArray.length; i++) {
            let current_check_obj = formInputArray[i]
            if (
                current_check_obj.length < 1 ||
                current_check_obj.country.length < 1 ||
                current_check_obj.start_date.length < 1 ||
                current_check_obj.end_date.length < 1
            ) {
                check_result = false
                break
            }
        }
        check_result === true ? addTask() : setDisplayCheckNotPassRemind(true)
    }

    const handleAddTaskClick = () => {
        setAllowAddTask(true)
        if (currentWindowSize.x <= 1000) {
            setShowAddTaskModal(true)
        }
    }

    const checkShowMobileNextBtn = (index) => {
        let display_element = null
        let nextButtonIndex = mobileInputCurrentIndex + 1
        if (index === 0 && showNextTaskBtn === true) {
            display_element = (
                <Button
                    style={{ marginRight: '0.65rem' }}
                    variant="outline-info"
                    id="next-button"
                    onClick={handleMobileNextClick}
                    disabled={disableSearchButton}
                >
                    Next
                </Button>
            )
        } else if (
            index > 0 &&
            index < 4 &&
            showNextTaskBtn === true &&
            formInputArray[nextButtonIndex] !== undefined
        ) {
            display_element = (
                <Button
                    style={{ marginRight: '0.65rem' }}
                    variant="outline-info"
                    id="next-button"
                    onClick={handleMobileNextClick}
                    disabled={disableSearchButton}
                >
                    Next
                </Button>
            )
        }
        return display_element
    }

    const checkShowMobileRemoveAndGoBackBtn = (index) => {
        let display_element = null
        if (index > 0) {
            display_element = (
                <div>
                    <Button
                        style={{ marginRight: '0.75rem' }}
                        variant="outline-danger"
                        id="go-back-button"
                        onClick={handleMobileRemoveClick}
                        disabled={disableSearchButton}
                    >
                        Remove
                    </Button>
                    <Button
                        style={{ marginRight: '0.35rem' }}
                        variant="outline-primary"
                        id="go-back-button"
                        onClick={handleMobileGobackClick}
                        disabled={disableSearchButton}
                    >
                        Go Back
                    </Button>
                </div>
            )
        }
        return display_element
    }

    const checkShowMobileAddBtn = (index) => {
        let display_element = null
        let nextButtonIndex = mobileInputCurrentIndex + 1
        if (index < 4 && formInputArray[nextButtonIndex] === undefined) {
            display_element = (
                <Button
                    variant="secondary"
                    id="add-button"
                    onClick={handleMobileAddClick}
                    disabled={disableSearchButton}
                >
                    Add
                </Button>
            )
        }
        return display_element
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
                        <Button variant="danger" id="add_task_button" onClick={handleAddTaskClick}>
                            Add Task
                        </Button>
                    </Col>
                </Row>
            )}

            {allowAddTask === true ? (
                currentWindowSize.x > 1000 ? (
                    formInputArray.map((x, i) => {
                        return (
                            <div key={i}>
                                {i > 0 ? <br /> : null}
                                <Row>
                                    <Col xs="3">
                                        <Form.Control
                                            type="text"
                                            placeholder="Enter Ticker"
                                            name="ticker"
                                            onChange={(e) => handleFormInputArray(e, i)}
                                            value={x.ticker}
                                            disabled={disableSearchButton}
                                        />
                                    </Col>
                                    <Col xs="auto">
                                        <Form.Control
                                            type="date"
                                            placeholder="Start Date"
                                            name="start_date"
                                            onChange={(e) => handleFormInputArray(e, i)}
                                            value={x.start_date}
                                            timeFormat="YYYY-MM-DD"
                                            disabled={disableSearchButton}
                                        />
                                    </Col>
                                    <Col xs="auto">
                                        <Form.Control
                                            type="date"
                                            name="end_date"
                                            placeholder="End Date"
                                            onChange={(e) => handleFormInputArray(e, i)}
                                            value={x.end_date}
                                            timeFormat="YYYY-MM-DD"
                                            disabled={disableSearchButton}
                                        />
                                    </Col>
                                    <Col xs="auto">
                                        <Form.Select
                                            disabled={disableSearchButton}
                                            name="country"
                                            value={x.country}
                                            onChange={(e) => handleFormInputArray(e, i)}
                                        >
                                            {countryOption.map((country) => {
                                                return (
                                                    <option key={country.id} value={country.value}>
                                                        {country.id}
                                                    </option>
                                                )
                                            })}
                                        </Form.Select>
                                    </Col>
                                    {i === 0 ? (
                                        <Col xs="auto">
                                            <Button
                                                variant="primary"
                                                id="search-button"
                                                onClick={handleSendSearch}
                                                disabled={disableSearchButton}
                                            >
                                                Search
                                            </Button>
                                        </Col>
                                    ) : null}
                                    <Col xs="auto">{allowActionAdd(i)}</Col>
                                    <Col xs="auto">
                                        <Button
                                            variant="danger"
                                            id="remove-button"
                                            onClick={handleRemoveClick.bind(null, i)}
                                            disabled={false}
                                        >
                                            Remove
                                        </Button>
                                    </Col>
                                </Row>
                            </div>
                        )
                    })
                ) : (
                    <Modal show={showAddTaskModal} onHide={handleMobileCloseAddTaskModal}>
                        <Modal.Header closeButton>
                            <Modal.Title>Add {mobileInputCurrentIndex + 1} task</Modal.Title>
                        </Modal.Header>

                        <Modal.Body>
                            <Form.Group className="mb-3" controlId="formBasicTicker">
                                <Form.Label>Search ticker</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="Enter Ticker"
                                    name="ticker"
                                    onChange={(e) => handleFormInputArray(e, mobileInputCurrentIndex)}
                                    value={formInputArray[mobileInputCurrentIndex].ticker}
                                    disabled={disableSearchButton}
                                />
                            </Form.Group>

                            <br />
                            <Form.Group className="mb-3" controlId="formBasicStartDate">
                                <Form.Label>Search Start Date</Form.Label>
                                <Form.Control
                                    type="date"
                                    placeholder="Start Date"
                                    name="start_date"
                                    onChange={(e) => handleFormInputArray(e, mobileInputCurrentIndex)}
                                    value={formInputArray[mobileInputCurrentIndex].start_date}
                                    timeFormat="YYYY-MM-DD"
                                    disabled={disableSearchButton}
                                />
                            </Form.Group>

                            <br />
                            <Form.Group className="mb-3" controlId="formBasicEndDate">
                                <Form.Label>Searh End Date</Form.Label>
                                <Form.Control
                                    type="date"
                                    name="end_date"
                                    placeholder="End Date"
                                    onChange={(e) => handleFormInputArray(e, mobileInputCurrentIndex)}
                                    value={formInputArray[mobileInputCurrentIndex].end_date}
                                    timeFormat="YYYY-MM-DD"
                                    disabled={disableSearchButton}
                                />
                            </Form.Group>

                            <br />
                            <Form.Group className="mb-3" controlId="formBasicCountry">
                                <Form.Label>Search Country</Form.Label>
                                <Form.Select
                                    disabled={disableSearchButton}
                                    name="country"
                                    onChange={(e) => handleFormInputArray(e, mobileInputCurrentIndex)}
                                    value={formInputArray[mobileInputCurrentIndex].country}
                                >
                                    {countryOption.map((country) => {
                                        return (
                                            <option key={country.id} value={country.value}>
                                                {country.id}
                                            </option>
                                        )
                                    })}
                                </Form.Select>
                            </Form.Group>
                        </Modal.Body>

                        <Modal.Footer>
                            {checkShowMobileRemoveAndGoBackBtn(mobileInputCurrentIndex)}
                            {checkShowMobileNextBtn(mobileInputCurrentIndex)}
                            {checkShowMobileAddBtn(mobileInputCurrentIndex)}
                            <Button
                                variant="primary"
                                id="search-button"
                                onClick={handleSendSearch}
                                disabled={disableSearchButton}
                            >
                                Search
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
                <Modal show={displayViewTaskContent} onHide={closeDisplayViewTaskResult} fullscreen={true}>
                    <Modal.Header closeButton>
                        <Modal.Title>{currentViewTaskId}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div>{viewInfoTableList()}</div>
                    </Modal.Body>
                </Modal>
            </Row>
            <Row>
                <Modal show={displayChart} onHide={closeDisplayChart} fullscreen={true}>
                    <Modal.Header closeButton>
                        <Modal.Title>{currentViewTaskId}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>{viewInfoChart()}</Modal.Body>
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
                    callBackViewTaskContentRows={setviewInfoContentRows}
                    callBackCurrentSelectedTaskId={setCurrentSelectedTaskId}
                    callBackDisplayViewTaskContent={setDisplayViewTaskContent}
                    callBackChartRows={setChartRows}
                    callBackDisplayChart={setDisplayChart}
                    callBackAnalysisType={setAnalysisType}
                    callBackChangeCurrentWindowSize={setCurrentWindowSize}
                />
            </Row>
        </Container>
    )
}
