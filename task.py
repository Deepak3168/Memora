# tasks.py
from concurrent.futures import ThreadPoolExecutor

# Create a single executor when server starts
executor = ThreadPoolExecutor(max_workers=5)
