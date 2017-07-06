import test_utilities
test_utilities.add_folders()
import utilities
import configuration


def test_0():

    try:
        cm = configuration.Config_Manager("af")
    except Exception as error:
        utilities.show_exception_info(error)

    try:
        cm.set_config_file_path(
            config_file_path="/home/sidharth/Dropbox/QM-Redesign/Configuration/config-0.yaml")
    except Exception as error:
        utilities.show_exception_info(error)

    try:
        config_dict = cm.read_config()
        print config_dict
    except Exception as error:
        utilities.show_exception_info(error)


test_0()
