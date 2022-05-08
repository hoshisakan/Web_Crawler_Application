import csv
# import xlsxwriter
import os
import json
from .handle_exception import HandleException

class FileOperation():
    def __init__(self, **file):
        self.__path = file['path']

    def __get_full_path(self, dirname):
        return os.path.join(self.__path, dirname)

    def __check_dir_is_exists(self, dir_path):
        if os.path.exists(dir_path):
            return True
        return False

    def __create_folder_by_path(self, path):
        if not self.__check_dir_is_exists(path):
            # os.mkdir(path)
            os.makedirs(path)

    def __check_exists(self, full_path):
        return os.path.exists(full_path)

    def __remove_file(self, full_path):
        if self.__check_exists(full_path):
            os.remove(full_path)

    def write_to_csv(self, dirname=None, filename=None, data=None):
        try:
            full_path = os.path.join(dirname, f"{filename}.csv")
            save_path = self.__get_full_path(dirname)
            self.__create_folder_by_path(save_path)
            with open(file=full_path,mode="w+",
                newline='',encoding="utf-8") as csvfile:
                csvfile.write('\ufeff')
                writer = csv.writer(csvfile)
                writer.writerows(data)
            return True
        except Exception as e:
            return HandleException.show_exp_detail_message(e)
    
    def write_to_json(self, dirname=None, filename=None, data=None):
        try:
            full_path = os.path.join(dirname, f"{filename}.json")
            save_path = self.__get_full_path(dirname)
            self.__create_folder_by_path(save_path)
            with open(file=full_path,mode="w+",
                newline='', encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            return HandleException.show_exp_detail_message(e)

    def remove_csv_and_json_files(self, csv_dir, json_dir, task_id):
        try:
            csv_dir_full_path = self.__get_full_path(csv_dir)
            json_dir_full_path = self.__get_full_path(json_dir)
            remove_csv_file_path = [os.path.join(csv_dir_full_path, filename) for filename in os.listdir(csv_dir_full_path) if filename.find(task_id) != -1]
            remove_json_file_path = [os.path.join(json_dir_full_path, filename) for filename in os.listdir(json_dir_full_path) if filename.find(task_id) != -1]
            if not remove_csv_file_path or not remove_json_file_path:
                return False
            self.__remove_file(remove_csv_file_path[0])
            self.__remove_file(remove_json_file_path[0])
            if self.__check_exists(remove_csv_file_path[0]) is False and self.__check_exists(remove_json_file_path[0]) is False:
                return True
            return False
        except Exception as e:
            return HandleException.show_exp_detail_message(e)
