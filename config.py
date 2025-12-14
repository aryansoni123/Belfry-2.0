"""
Configuration file for Belfry application.
"""
import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'belfry-secret-key-change-in-production-2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///belfry.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Docker configuration for code execution (LeetCode-style)
    DOCKER_IMAGE = 'python:3.13-slim'
    DOCKER_TIMEOUT = 2  # seconds per test case
    DOCKER_MEMORY_LIMIT = '256m'  # Memory limit per container
    DOCKER_CPU_QUOTA = 50000  # 50% CPU

