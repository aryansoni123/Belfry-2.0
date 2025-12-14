"""
Quick script to restore all quizzes if they're missing.
This script will recreate the database and add all sample quizzes.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seed_sample_data import seed_sample_data

if __name__ == '__main__':
    print("Restoring quizzes and sample data...")
    seed_sample_data()
    print("\nDone! All quizzes have been restored.")

