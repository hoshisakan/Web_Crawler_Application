import Chart from 'react-google-charts'
import { Container, Row } from 'react-bootstrap'

export default function LineChart(props) {
    const width = props.width
    const height = props.height
    const data = props.data
    const hAxisTitle = props.hAxisTitle === undefined ? 'Default hAxisTitle' : props.hAxisTitle
    const vAxisTitle = props.vAxisTitle === undefined ? 'Default vAxisTitle' : props.vAxisTitle
    const chartType = props.chartType === undefined ? 'LineChart' : props.chartType

    return (
        <Container fluid>
            <Row>
                <Chart
                    width={width}
                    height={height}
                    chartType={chartType}
                    loader={<div>Loading Chart</div>}
                    data={data}
                    options={{
                        hAxis: {
                            title: hAxisTitle,
                        },
                        vAxis: {
                            title: vAxisTitle,
                        },
                        series: {
                            1: { curveType: 'function' },
                        },
                    }}
                    rootProps={{ 'data-testid': '2' }}
                />
            </Row>
        </Container>
    )
}
