from pprint import pprint
import sys

sys.path.append('..')

from utils.client import (
    api_auto_ope_cycle_count,
    api_machine_list,
    api_tool_info_plc)


def test_api_auto_ope_cycle_count():
    ret = api_auto_ope_cycle_count()
    pprint(ret)
    return None

def test_api_machine_list():
    ret = api_machine_list()
    pprint(ret)
    return None

def test_api_tool_info_plc():
    ret = api_tool_info_plc(machine="CB4010-1")
    pprint(ret)
    return None


if __name__ == '__main__':
    # test_api_auto_ope_cycle_count()
    test_api_tool_info_plc()