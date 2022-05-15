import React from 'react'
import { Button, Table } from 'react-bootstrap'

export default function ViewNewsInfoTable(props) {
    const viewInfoTableRows = props.viewInfoTableRows === undefined ? [] : props.viewInfoTableRows
    const viewInfoTableCols = props.viewInfoTableCols === undefined ? [] : props.viewInfoTableCols
    const viewInfoTableSize = props.viewInfoTableSize === undefined ? 'lg' : props.viewInfoTableSize
    const viewInfoTableResponsive = props.viewInfoResponsive === undefined ? 'sm' : props.viewInfoTableResponsive

    return (
        <div>
            <Table responsive={viewInfoTableResponsive} striped bordered hover size={viewInfoTableSize}>
                <thead>
                    <tr>
                        {viewInfoTableCols.map((column, index) => {
                            return (
                                <th key={index} className="border-0">
                                    {column.headerName}
                                </th>
                            )
                        })}
                    </tr>
                </thead>
                <tbody>
                    {viewInfoTableRows.map((row, index) => {
                        return (
                            <tr key={index}>
                                <td>{row.title}</td>
                                <td>{row.summary}</td>
                                <td>{row.updated_time}</td>
                                <td>{row.newspaper}</td>
                                <td>
                                    <Button
                                        className="button-spacing-0"
                                        href={row.url}
                                        target="_blank"
                                        variant="secondary"
                                    >
                                        Link
                                    </Button>
                                </td>
                                <td>{row.search_page}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </div>
    )
}
