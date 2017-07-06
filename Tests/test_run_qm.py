import test_utilities
test_utilities.add_folders()
import utilities
import run_qm
import configuration
import super_queue
import counter


def test_0():
    try:
        cm = configuration.Config_Manager()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        cm.set_config_file_path(
            config_file_path="/home/sidharth/Dropbox/QM-Redesign/Configuration/config-0.yaml")
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        sq = super_queue.Super_Queue(["Type A", "Type B"])
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        counter_x = counter.Counter("Test Counter", ["Type A", "Type B"])
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        run_qm.service_counter(counter_x, sq)
    except Exception as error:
        utilities.show_exception_info(error)


test_0()
