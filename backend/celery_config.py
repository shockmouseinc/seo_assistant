# Broker settings
broker_url = 'redis://localhost:6379/0'

# List of modules to import when the Celery worker starts
imports = ('backend.tasks',)

# Using the database to store task state and results
result_backend = 'redis://localhost:6379/1'
