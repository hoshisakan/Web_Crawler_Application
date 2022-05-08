import React from 'react'
import { Card } from 'react-bootstrap'
import TableComponent from '../Table/Table';


export default function TableCard(props) {
    const cardTitle = props.cardTitle === undefined ? 'default title' : props.cardTitle
    const cardSubTitle = props.cardSubTitle === undefined ? 'default subtitle' : props.cardSubTitle
    const cardTextColor = props.cardTextColor === undefined ? 'black' : props.cardTextColor
    const cardHeaderColor = props.cardHeaderColor === undefined ? 'light' : props.cardHeaderColor
    const tableRows = props.tableRows === undefined ? [] : props.tableRows
    const tableColumns = props.tableColumns === undefined ? [] : props.tableColumns
    const tableSize = props.tableSize === undefined ? "sm" : props.tableSize
    const tableColor = props.tableColor === undefined ? "light" : props.tableColor

    return (
        <div>
            <Card className="strpied-tabled-with-hover" text={cardTextColor} bg={cardHeaderColor}>
                <Card.Header>
                    <Card.Title as="h4">{cardTitle}</Card.Title>
                    <p className="card-category">{cardSubTitle}</p>
                </Card.Header>
                <Card.Body className="table-full-width table-responsive px-0">
                    <TableComponent
                        columns={tableColumns} rows={tableRows}
                        tableSize={tableSize} tableColor={tableColor}
                    />
                </Card.Body>
            </Card>
        </div>
    )
}
