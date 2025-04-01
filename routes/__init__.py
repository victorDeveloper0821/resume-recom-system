from flask import Blueprint

# 建立 Blueprint
resume_bp = Blueprint('resume', __name__)

# 匯入各個 API 路由
from . import resume_routes