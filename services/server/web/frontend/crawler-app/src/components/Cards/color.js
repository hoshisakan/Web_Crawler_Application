export const color = [
    '#28bf28',
    '#ff0000',
    '#0000ff',
    '#1e90ff',
    '#ffa500',
    '#800080',
    '#000080',
    '#0047ab',
    '#ff8c00',
    '#1e90ff',
    '#9acd32',
    '#ff1493',
    '#0000cd',
    '#fa8072',
    '#d2b48c',
    '#9932cc',
    '#4b0082',
    '#d19fe8',
    '#efcc00',
    '#ff7f50',
    '#fe5a1d',
    '#9b111e',
    '#7f1734',
    '#ffc40c',
    '#ff4500',
    '#ffb347',
    '#00bfff',
    '#77b5fe',
    '#4166f5',
    '#5b92e5',
    '#318ce7',
    '#6495ed',
    '#191970',
    '#00008b',
]

// const randomHeaderColor = Math.floor(Math.random() * headerColor.length)

// Math.floor(Math.random() * range), generate range index of color
export const randomColor = () => {
    return color[Math.floor(Math.random() * color.length)]
}
