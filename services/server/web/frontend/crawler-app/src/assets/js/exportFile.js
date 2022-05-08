import { convertToLocalDate } from '../../components/Timer/dateFormat'

export const exportRequestFile = (export_data, task_id, file_type) => {
    let file_downloader = require('js-file-download')
    let full_filename = convertToLocalDate(new Date().toDateString()) + `_${task_id}.${file_type}`
    file_downloader(export_data, full_filename)
}