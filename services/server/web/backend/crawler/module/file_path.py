import os

class File():
    @staticmethod
    def remove_file(full_path):
        try:
            os.remove(full_path)
        except OSError:
            print(f"Remove file {full_path} failed. . .")
        else:
            print(f"Remove file {full_path} successfully!")

    @staticmethod
    def create_directory(full_path):
        try:
            # os.mkdir(full_path)
            os.makedirs(full_path)
        except OSError:
            print(f"Created directory {full_path} failed. . .")
            return False
        else:
            print("Created directory successfully!")
            return True

    @staticmethod
    def check_file_exists(full_path):
        return os.path.exists(full_path)

    @classmethod
    def combine_path(cls,**file):
        if file['mode'] is True:
            check_path = os.path.join(file['working_path'], file['dirname'])
            if cls.check_file_exists(check_path) is False:
                create_result = cls.create_directory(check_path)
                if create_result is False:
                    return None
            return os.path.join(file['working_path'], file['dirname'], file['name'])
        return os.path.join(file['working_path'], file['name'])

    @staticmethod
    def get_current_path():
        return os.getcwd()
