import React, { useState } from 'react'
import { Button, Table, Modal, Dropdown } from 'react-bootstrap'
import {
    apiTaskRemoveAllInfoResquest,
    apiObtainTaskGoogleSearchNews,
    apiExportGoogleSearchNewsResult,
    apiObtainTaskGoogleSearchVideo,
    apiExportGoogleSearchVideoResult
} from '../../../api.js'
import { convertToLocalDateTime } from '../../../components/Timer/dateFormat'
import { exportRequestFile } from '../../../assets/js/exportFile.js'
import { exportFileOptions } from '../../../views/google_search/dropdown_options'

export default function TaskTableList(props) {
    const {
        taskTableRows,
        taskTableCols,
        taskTableSize,
        taskTableResponsive,
        callBackViewTaskResultRows,
        callBackCurrentViewTaskId,
        callBackDisplayViewTaskResult,
        callBackCurrentViewDataType,
        // callBackUpdateTaskProgress,
    } = props
    const [displayDeleteConfirm, setDisplayDeleteConfirm] = useState(false)
    const [selectedTaskId, setSelectedTaskId] = useState('')
    // const [selectedId, setSelectedId] = useState('')
    // const [selectedTaskStatus, setSelectedTaskStatus] = useState('')
    const [selectedDataType, setSelectedDataType] = useState('')

    const handleViewTaskContent = async (task_id, data_type) => {
        // console.log(data_type)
        if (data_type === 'google news') {
            await apiObtainTaskGoogleSearchNews(task_id)
                .then((res) => {
                    let data = res.data
                    // console.log(data)
                    callBackViewTaskResultRows(data)
                    callBackCurrentViewTaskId(task_id)
                    callBackDisplayViewTaskResult(true)
                    callBackCurrentViewDataType(data_type)
                })
                .catch((err) => {
                    console.error('Error: ' + err.message)
                })
        } else if (data_type === 'google video') {
            await apiObtainTaskGoogleSearchVideo(task_id)
                .then((res) => {
                    let data = res.data
                    // console.log(data)
                    callBackViewTaskResultRows(data)
                    callBackCurrentViewTaskId(task_id)
                    callBackDisplayViewTaskResult(true)
                    callBackCurrentViewDataType(data_type)
                })
                .catch((err) => {
                    console.error('Error: ' + err.message)
                })
        }
    }

    const handleDeleteItemEvent = async () => {
        // console.log(
        //     `will be remove the ${selectedTaskId} that task status is: ${selectedTaskStatus} and data type is: ${selectedDataType}`
        // )
        apiTaskRemoveAllInfoResquest(selectedTaskId)
            .then((res) => {
                // console.log(res.data)
            })
            .catch((err) => {
                console.error(err.message)
            })
        // callBackUpdateTaskProgress(true)
        closeDeleteItemConfirm()
    }

    const closeDeleteItemConfirm = () => {
        setDisplayDeleteConfirm(false)
    }

    const displayDeleteItemConfirm = (task_id) => {
        setSelectedTaskId(task_id)
        setDisplayDeleteConfirm(true)
    }

    const updateSelectedTaskItem = (task_id, data_type) => {
        setSelectedTaskId(task_id)
        setSelectedDataType(data_type)
    }

    const handleExportOptionChange = (eventKey, event) => {
        let file_type = exportFileOptions[eventKey].value.toLowerCase()
        // console.log(
        //     `Selected task id: ${selectedTaskId}, Selected data type: ${selectedDataType}, File type: ${file_type}`
        // )
        if (selectedDataType === 'google news') {
            apiExportGoogleSearchNewsResult(selectedTaskId, file_type)
                .then((res) => {
                    let data = res.data
                    exportRequestFile(data, selectedTaskId, file_type)
                })
                .catch((err) => {
                    console.error(err.message)
                })
        } else if (selectedDataType === 'google video') {
            apiExportGoogleSearchVideoResult(selectedTaskId, file_type)
                .then((res) => {
                    let data = res.data
                    exportRequestFile(data, selectedTaskId, file_type)
                })
                .catch((err) => {
                    console.error(err.message)
                })
        }
    }

    return (
        <div>
            <Modal show={displayDeleteConfirm} backdrop="static" keyboard={false}>
                <Modal.Header style={{ background: 'red', color: 'white' }}>
                    <Modal.Title>
                        <p>Confirm delete</p>
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Are you sure you want to delete the task
                    <span style={{ fontWeight: 'bold' }}> {selectedTaskId}</span> ?
                </Modal.Body>
                <Modal.Footer style={{ borderColor: 'red' }}>
                    <Button variant="primary" onClick={handleDeleteItemEvent}>
                        Yes
                    </Button>
                    <Button variant="secondary" onClick={closeDeleteItemConfirm}>
                        No
                    </Button>
                </Modal.Footer>
            </Modal>
            <Table responsive={taskTableResponsive} striped bordered hover size={taskTableSize}>
                <thead>
                    <tr>
                        {taskTableCols.map((column, index) => {
                            return (
                                <th key={index} className="border-0">
                                    {column.headerName}
                                </th>
                            )
                        })}
                    </tr>
                </thead>
                <tbody>
                    {taskTableRows.map((row, index) => {
                        return (
                            <tr key={index}>
                                {/* <td>{row.id}</td> */}
                                <td>{row.task_id}</td>
                                <td>{row.task_mark}</td>
                                <td>{row.data_source}</td>
                                <td>{row.data_type}</td>
                                <td>{row.status}</td>
                                <td>{convertToLocalDateTime(row.date_done)}</td>
                                {/* <td>{row.task_name}</td> */}
                                {/* <td>{convertToLocalDateTime(row.date_created)}</td> */}
                                <td>
                                    {row.status === 'SUCCESS' ? (
                                        <div>
                                            <Button
                                                className="button-spacing-0"
                                                variant="secondary"
                                                onClick={handleViewTaskContent.bind(null, row.task_id, row.data_type)}
                                            >
                                                View
                                            </Button>
                                        </div>
                                    ) : null}
                                </td>
                                <td>
                                    {row.status === 'SUCCESS' ? (
                                        <div>
                                            <Dropdown
                                                onClick={updateSelectedTaskItem.bind(null, row.task_id, row.data_type)}
                                                onSelect={handleExportOptionChange}
                                            >
                                                <Dropdown.Toggle id="dropdown-button-dark-example1" variant="success">
                                                    Export
                                                </Dropdown.Toggle>

                                                <Dropdown.Menu variant="dark">
                                                    {exportFileOptions.map((options, index) => {
                                                        return (
                                                            <Dropdown.Item key={options.id} eventKey={index}>
                                                                <span>{options.value}</span>
                                                            </Dropdown.Item>
                                                        )
                                                    })}
                                                </Dropdown.Menu>
                                            </Dropdown>
                                            {/* <Button
                                                className="button-spacing-0"
                                                onClick={handleExportSpecificFile.bind(
                                                    null,
                                                    row.task_id,
                                                    'csv',
                                                    row.data_type
                                                )}
                                                variant="success"
                                            >
                                                CSV
                                            </Button>
                                            <Button
                                                className="button-spacing-0"
                                                onClick={handleExportSpecificFile.bind(
                                                    null,
                                                    row.task_id,
                                                    'json',
                                                    row.data_type
                                                )}
                                                variant="warning"
                                            >
                                                JSON
                                            </Button> */}
                                        </div>
                                    ) : null}
                                </td>
                                <td>
                                    <div>
                                        <Button
                                            className="button-spacing-0"
                                            variant="danger"
                                            onClick={displayDeleteItemConfirm.bind(
                                                null,
                                                row.task_id
                                            )}
                                        >
                                            Delete
                                        </Button>
                                    </div>
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </div>
    )
}
