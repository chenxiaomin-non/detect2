import sys
import os
if sys.path[-1] != os.path.dirname(os.path.abspath(__file__)):
    sys.path.append(os.path.dirname(sys.path[0]))
print(sys.path)