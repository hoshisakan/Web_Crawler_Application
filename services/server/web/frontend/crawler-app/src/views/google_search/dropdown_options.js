export const taskResultColumns = [
    // { field: 'id', headerName: 'id' },
    { field: 'task_id', headerName: 'task_id' },
    { field: 'task_mark', headerName: 'task_mark' },
    { field: 'data_source', headerName: 'data_source' },
    { field: 'data_type', headerName: 'data_type' },
    { field: 'status', headerName: 'status' },
    { field: 'date_done', headerName: 'date_done' },
    // { field: 'task_name', headerName: 'task_name' },
    // { field: 'date_created', headerName: 'date_created' },
    { field: 'view', headerName: 'view' },
    { field: 'download', headerName: 'download' },
    { field: 'action', headerName: 'action' },
]

export const viewNewsInfoColumns = [
    // { field: 'task_id', headerName: 'task_id' },
    { field: 'title', headerName: 'title' },
    { field: 'summary', headerName: 'summary' },
    { field: 'updated_time', headerName: 'updated_time' },
    { field: 'newspaper', headerName: 'newspaper' },
    { field: 'url', headerName: 'url' },
    { field: 'search_page', headerName: 'search_page' },
]

export const viewVideoInfoColumns = [
    // { field: 'task_id', headerName: 'task_id' },
    { field: 'title', headerName: 'title' },
    { field: 'summary', headerName: 'summary' },
    { field: 'updated_time', headerName: 'updated_time' },
    { field: 'uploader', headerName: 'uploader' },
    { field: 'video_length', headerName: 'video_length' },
    { field: 'url', headerName: 'url' },
    { field: 'search_page', headerName: 'search_page' },
]

export const dataTypeOptions = [
    { id: 'None', value: 'Select Data Type' },
    { id: 'news', value: 'google news' },
    { id: 'video', value: 'google video' },
]

export const exportFileOptions = [
    { id: 1, value: 'CSV' },
    { id: 2, value: 'JSON' },
]
