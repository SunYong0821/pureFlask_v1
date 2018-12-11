# -*- coding: utf-8 -*-
from flask import Blueprint

tools = Blueprint('tools', __name__)

from app.tools import tools_views
