import pandas as pd
import numpy as np
from datetime import datetime
from os import walk


# read in all coha corpus text files, concatenate into a giant string
filenames = next(walk('../data/coha_sample'), (None, None, []))[2]  # [] if no file
