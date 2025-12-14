"""
Authentication blueprint for Belfry.
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from auth import routes

