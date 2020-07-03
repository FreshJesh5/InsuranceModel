import pandas as pd
from numpy import savetxt
import numpy as np

import numpy as np
import pandas as pd

arr = [0,1,2]
arr2 = [0.0,0.1,0.2]

pd1 = pd.DataFrame(arr, columns=['Val'])
pd2 = pd.DataFrame(arr2, columns=['Val'])


print((pd1['Val']*pd2['Val']).sum())
