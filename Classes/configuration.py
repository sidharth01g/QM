import yaml
import os
import utilities


class Config_Manager:
    """
    Performs operations related to config file
    """
    def __init__(self, config_file_path=""):
        try:
            if type(config_file_path) is not str:
                raise Exception("Class Config_Manager- __init__(..): " +
                                "config_file_path not of type str")

            self.config_file_path = config_file_path
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_config_file_path(self, config_file_path):
        """
        Setter function for config_file_path
        """
        try:
            if type(config_file_path) is not str:
                raise Exception("Class Config_Manager- " +
                                "set_config_file_path(..): " +
                                "config_file_path not of type str")

            self.config_file_path = config_file_path
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def read_config(self):
        """
        Reads config file specified by self.config_file_path
        """
        try:
            config_dict = None
            if not os.path.exists(self.config_file_path):
                raise Exception("Class Config_Manager- read_config(..): " +
                                self.config_file_path + " does not exist")
            with open(self.config_file_path, 'r') as stream:
                try:
                    config_dict = yaml.load(stream)
                    # print(type(config_dict))
                except yaml.YAMLError as exc:
                    print(exc)
            return config_dict
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def validate_config(self):
        """
        To-Do: Validate config file
        """
        return
