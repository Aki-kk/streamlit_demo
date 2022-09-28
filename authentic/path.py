import io
import json
import os
import numpy as np
import pandas as pd
import numpy as np
import requests
from PIL import Image
from pandas.core.frame import DataFrame


bytes_data = requests.get(f"http://127.0.0.1:8000/pic")