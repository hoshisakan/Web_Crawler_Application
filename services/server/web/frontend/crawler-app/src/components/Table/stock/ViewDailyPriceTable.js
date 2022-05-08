import React from 'react'
import { Table } from 'react-bootstrap'

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
                                <td>{row.ticker}</td>
                                <td>{row.trade_date}</td>
                                <td>{row.open_price}</td>
                                <td>{row.high_price}</td>
                                <td>{row.low_price}</td>
                                <td>{row.close_price}</td>
                                <td>{row.adj_close_price}</td>
                                <td>{row.volume}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </div>
    )
}
