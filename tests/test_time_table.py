from chombopy.time_table import TimeTable, TimeTableMethod
import os
import logging
import unittest

LOGGER = logging.getLogger(__name__)


def test_time_table_method():
    ttm = TimeTableMethod("")
    assert ttm.valid == False

    ttm = TimeTableMethod(
        "  [562] Class::method 0.01144  0.1% 50 0 0 MFlops ", parent_el="Parent"
    )

    assert ttm.parent == "Parent"
    assert ttm.valid == True
    assert ttm.indent == 2
    assert ttm.id == 562
    assert ttm.name == "Class::method"
    assert ttm.time == 0.01144

    assert ttm.long_desc() == "[562] Class::method (0.01144)"

    assert str(ttm) == "Class::method"


class TestTimeTable(unittest.TestCase):
    def test_time_table(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(this_dir, "data/time.table.simple")

        tt = TimeTable(file_path)

        assert tt.filepath == file_path

        methods = tt.methods

        LOGGER.info(methods)

        assert len(tt.methods) == 8
        assert tt.methods[7].name == "Program::someOtherMethod"

        # == ['program',
        #                'AMR::run',
        #                'AMR::timeStep',
        #                'Program::method',
        #                'AMR::timeStep::postTimeStep',
        #                'AMR::timeStep::newDt',
        #                'Program::method',
        #                'Program::someOtherMethod']

        children = tt.get_all_children("AMR::timeStep")
        assert len(children.keys()) == 2

        second_parent_key = list(children.keys())[1]
        assert second_parent_key.name == "AMR::timeStep"
        assert len(children[second_parent_key]) == 1
        assert children[second_parent_key][0].name == "Program::method"

        assert len(tt.get_all_children("AMR::timeStep")) == 2

        assert tt.total_time_in_method("program") == 8.80352
        assert tt.total_time_in_method("AMR::timeStep") == 5.87694 + 0.02004

        call_history_program = tt.get_call_history_for_id(1)
        assert len(call_history_program) == 2
        assert call_history_program[0].name == "main"

        call_history_program_method = tt.get_call_history_for_id(1400)
        assert len(call_history_program_method) == 4
        assert call_history_program_method[0].name == "main"
        assert call_history_program_method[1].name == "AMR::timeStep::postTimeStep"
        assert call_history_program_method[2].name == "AMR::timeStep"

        call_history_program_method = tt.get_call_history_for_name("Program::method")
        assert len(call_history_program_method) == 2
        assert call_history_program_method[0][0].name == "main"
        assert call_history_program_method[0][1].name == "program"
        assert call_history_program_method[0][2].name == "AMR::timeStep"

        assert call_history_program_method[1][0].name == "main"
        assert call_history_program_method[1][1].name == "AMR::timeStep::postTimeStep"
        assert call_history_program_method[1][2].name == "AMR::timeStep"
