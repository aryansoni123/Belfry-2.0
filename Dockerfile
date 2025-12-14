# Dockerfile for LeetCode-style code execution sandbox
FROM python:3.13-slim

WORKDIR /app

# Install only essential packages
# No network access, no extra tools
# Minimal image for security

# This image is used by judge.py for secure code execution
# Each submission runs in an isolated container instance
# Container is destroyed after execution

