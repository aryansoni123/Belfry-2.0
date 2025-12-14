"""
Teacher blueprint for Belfry.
"""
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__)

from teacher import routes

