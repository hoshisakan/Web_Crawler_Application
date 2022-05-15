import os
from os import walk


check_exists = lambda check_path: os.path.exists(check_path)

output_path_list = [os.getcwd(), os.path.dirname(__file__), os.path.abspath(__file__), os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))]

output_path = None

for index, path in enumerate(output_path_list, 1):
    # print(f'The {index} read path is: {path}')
    if check_exists(path):
        output_path = os.path.join(path, 'output')

# print(f"Found path: {output_path}") if check_exists(output_path) else print('Not found path')

delete_task_id = '2ff8c17c-b188-44dc-a0dd-0668bb251a10'

def checkPathDirFilesExists():
    if check_exists(output_path):
        csv_dir_path = os.path.join(output_path, 'csv')
        json_dir_path = os.path.join(output_path, 'json')
        csv_remove_res = False
        json_remove_res = False

        #TODO if csv and json directory files count not same, then can't be use zip iterable, should use two for loop iterable csv and json directory files
        csv_remove_res = [True for filename in os.listdir(csv_dir_path) if filename.find(delete_task_id) != -1][0]
        json_remove_res = [True for filename in os.listdir(json_dir_path) if filename.find(delete_task_id) != -1][0]

        print(csv_remove_res, json_remove_res)

        #TODO if csv and json directory files count same, then can be use zip iterable
        for csv, json in zip(os.listdir(csv_dir_path), os.listdir(json_dir_path)):
            if csv.find(delete_task_id) != -1 and json.find(delete_task_id) != -1:
                # print(f'Remove csv and json the task id is: {delete_task_id}')
                csv_remove_res = True
                json_remove_res = True
                break
            # else:
            #     print(f'Not found any match items.')
        
        print(csv_remove_res, json_remove_res)

def removePathDirFiles():
    if check_exists(output_path):
        csv_dir_path = os.path.join(output_path, 'csv')
        json_dir_path = os.path.join(output_path, 'json')

        #TODO if csv and json directory files count not same, then can't be use zip iterable, should use two for loop iterable csv and json directory files
        [os.remove(os.path.join(csv_dir_path, filename)) for filename in os.listdir(csv_dir_path) if filename.find(delete_task_id) != -1]
        [os.remove(os.path.join(json_dir_path, filename)) for filename in os.listdir(json_dir_path) if filename.find(delete_task_id) != -1]

        #TODO if csv and json directory files count same, then can be use zip iterable
        # for csv_files, json_files in zip(os.listdir(csv_dir_path), os.listdir(json_dir_path)):
        #     if csv_files.find(delete_task_id) != -1 and json_files.find(delete_task_id) != -1:
        #         os.remove(os.path.join(csv_dir_path, csv_files))
        #         os.remove(os.path.join(json_dir_path, json_files))
        #         break

def main():
    # checkPathDirFilesExists()
    removePathDirFiles()

if __name__ == "__main__":
    main()