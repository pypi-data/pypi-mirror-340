
# IMPORT SoftwareAI Libs 
from CoreEngine.CoreInicializer._init_libs_ import *
import re
from pydantic import BaseModel
from firebase_admin import App
import importlib

class TitleAndPreface(BaseModel):
    title: str
    preface: str
