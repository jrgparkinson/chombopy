import os
from pathlib import Path
from chombopy.time_table import TimeTable

chombopy_home = Path(__file__).resolve().parents[1]
filepath = os.path.join(chombopy_home, 'tests', 'data', 'time.table.0')

print('Example usage with file: %s' % filepath)

time_table = TimeTable(filepath)

method_name = 'AMRNonLinearMultiCompOp::levelGSRB::BCs'
parent_children = time_table.get_all_children(method_name)

print('Children of %s\n' % method_name)
for parent in list(parent_children.keys()):
    print(parent.long_desc())
    for c in parent_children[parent]:
        print('  %s' % c.long_desc())

print('Total time in %s: %.3g' % (method_name, time_table.total_time_in_method(method_name)))

print('Call histories for %s:' % method_name)
call_histories = time_table.get_call_history_for_name(method_name)

for c in call_histories:
    print(' -> '.join(['%s' % m for m in c]) + '\n')

# Compare multiple files
files = []
tt = [TimeTable(f) for f in files]