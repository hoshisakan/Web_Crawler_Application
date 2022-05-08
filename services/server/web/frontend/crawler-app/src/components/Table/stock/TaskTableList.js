import React, { useState } from 'react'
import { Button, Table, Modal, Dropdown } from 'react-bootstrap'
import {
    apiFilterStockInfo,
    apiExportStockInfo,
    apiTaskRemoveAllInfoResquest,
    apiChartStockInfo,
} from '../../../api.js'
import { convertToLocalDateTime } from '../../../components/Timer/dateFormat'
import { exportRequestFile } from '../../../assets/js/exportFile.js'
import { getCurrentWindowSize } from '../../../assets/js/getWindowSize.js'
import {
    exportFileOptions,
    chartStockInfoColumns,
    chartStockInfoMulColumns,
} from '../../../views/stock/dropdown_options'

export default function TaskTableList(props) {
    const {
        taskTableRows,
        taskTableCols,
        taskTableSize,
        taskTableResponsive,
        callBackViewTaskContentRows,
        callBackCurrentSelectedTaskId,
        callBackDisplayViewTaskContent,
        callBackChartRows,
        callBackDisplayChart,
        callBackAnalysisType,
        callBackChangeCurrentWindowSize
        // callBackUpdateTaskProgress,
    } = props
    const [displayDeleteConfirm, setDisplayDeleteConfirm] = useState(false)
    const [selectedTaskId, setSelectedTaskId] = useState('')
    const [selectedTaskIsMultiple, setSelectedTaskIsMultiple] = useState(false)

    const handleViewTaskContent = async (task_id, data_type) => {
        await apiFilterStockInfo(task_id)
            .then((res) => {
                let data = res.data
                // console.log(data)
                callBackViewTaskContentRows(data)
                callBackCurrentSelectedTaskId(task_id)
                callBackDisplayViewTaskContent(true)
            })
            .catch((err) => {
                console.error('Error: ' + err.message)
            })
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
        // setSelectedDataType(data_type)
    }

    const handleExportOptionChange = (eventKey, event) => {
        let file_type = exportFileOptions[eventKey].value.toLowerCase()
        console.log(file_type)
        apiExportStockInfo(selectedTaskId, file_type)
            .then((res) => {
                let data = res.data
                exportRequestFile(data, selectedTaskId, file_type)
            })
            .catch((err) => {
                console.error(err)
            })
    }

    const updateAnalysisSelectedTaskItem = (task_id, data_type, is_multiple) => {
        setSelectedTaskId(task_id)
        setSelectedTaskIsMultiple(is_multiple)
        // console.info(selectedTaskId)
        callBackChangeCurrentWindowSize(getCurrentWindowSize())
    }

    const handleAnalysisOptionChange = (eventKey, event) => {
        let search_type = ''
        let filter_condition = ''

        if (selectedTaskIsMultiple === true) {
            search_type = chartStockInfoMulColumns[eventKey].id
            filter_condition = 'multiple'
            callBackAnalysisType(chartStockInfoMulColumns[eventKey].value)
        } else {
            search_type = chartStockInfoColumns[eventKey].id
            filter_condition = 'single'
            callBackAnalysisType(chartStockInfoColumns[eventKey].value)
        }

        apiChartStockInfo(selectedTaskId, search_type, filter_condition)
            .then((res) => {
                let data = res.data
                // console.log(data)
                // const newData = data.slice(0)
                // for (var i = 1; i < data.length; i++) {
                //     data[i][0] = new Date(data[i][0])
                // }
                callBackChartRows(data)
                callBackCurrentSelectedTaskId(selectedTaskId)
                callBackDisplayChart(true)
            })
            .catch((err) => {
                console.log(err.message)
            })
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
                                        </div>
                                    ) : null}
                                </td>
                                <td>
                                    {row.status === 'SUCCESS' ? (
                                        <div>
                                            <Dropdown
                                                onClick={updateAnalysisSelectedTaskItem.bind(
                                                    null,
                                                    row.task_id,
                                                    row.data_type,
                                                    row.is_multiple
                                                )}
                                                onSelect={handleAnalysisOptionChange}
                                            >
                                                <Dropdown.Toggle
                                                    id="dropdown-button-dark-analysis"
                                                    variant="outline-primary"
                                                >
                                                    Analysis
                                                </Dropdown.Toggle>

                                                <Dropdown.Menu variant="dark">
                                                    {row.is_multiple === true
                                                        ? chartStockInfoMulColumns.map((options, index) => {
                                                              return (
                                                                  <Dropdown.Item key={options.id} eventKey={index}>
                                                                      <span>{options.value}</span>
                                                                  </Dropdown.Item>
                                                              )
                                                          })
                                                        : chartStockInfoColumns.map((options, index) => {
                                                              return (
                                                                  <Dropdown.Item key={options.id} eventKey={index}>
                                                                      <span>{options.value}</span>
                                                                  </Dropdown.Item>
                                                              )
                                                          })}
                                                </Dropdown.Menu>
                                            </Dropdown>
                                        </div>
                                    ) : null}
                                </td>
                                <td>
                                    <div>
                                        <Button
                                            className="button-spacing-0"
                                            variant="danger"
                                            onClick={displayDeleteItemConfirm.bind(null, row.task_id)}
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
