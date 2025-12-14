"""
Student blueprint for Belfry.
"""
from flask import Blueprint

student_bp = Blueprint('student', __name__)

from student import routes

