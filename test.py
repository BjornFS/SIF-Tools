
from SIFpy import sif2array
import os

file = os.path.abspath('/Users/bjornfunchschroder/Desktop/Bjørn/WSe2Mono_SHG_150lw_1point7mW_20s.sif')
data = sif2array(target=file, reduce_noise=False, window='narrow').get_data()
print(data)