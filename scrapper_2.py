import math
import requests
from bs4 import BeautifulSoup
#import re
import pandas as pd

from material_class import ParamMats
param_mat_obj = ParamMats()

if __name__ == "__main__":
    param_mat_obj.create_material_curve_csvs()
