import logging
from datetime import datetime

# from shared.base.mongo_db import MongoDBConnection

# mongo_service = MongoDBConnection(maxPoolSize=5)

class EdgeAppLogger:
    def __init__(self, name, log_file='app.log', log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create formatter for log messages
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # # MongoDB handler
        # self.mongo_handler = MongoDBHandler()
        # self.mongo_handler.setFormatter(formatter)
        # # -- as an option, not added to logger

    def log(self, message, level=logging.INFO, log_to_mongodb=False):
        self.logger.log(level, message)
        if log_to_mongodb:
            record = self.logger.makeRecord(self.logger.name, level, None, None, message, None, None)
            # self.mongo_handler.emit(record)


# class MongoDBHandler(logging.Handler):
#     DATABASE_NAME = 'DeviceControl'
#     COLLECTION_NAME = 'Log'
#     COLLECTION_META = {
#         "TimeField": "TimeStamp",
#         "MetaField": "Meta",
#         "Granularity": "seconds",
#         "ExpireAfterSeconds": 2592000, # 1 month
#         "Indexes": [
#             [("TimeStamp", 1)],
#         ],
#     }
#     BATCH_SIZE = 1 # ! Adjust for insertion efficiency

#     def __init__(self):
#         super().__init__()
#         mongo_service.init_time_series_collection(
#             database_name=self.DATABASE_NAME,
#             collection_name=self.COLLECTION_NAME,
#             collection_meta=self.COLLECTION_META,
#         )
#         self.database = mongo_service.get_database(self.DATABASE_NAME)
#         self.collection = mongo_service.get_collection(self.database, self.COLLECTION_NAME)

#         self.buffer = []
#         self.buffer_size = 10  # Set buffer size for batch insertion

#     def emit(self, record):
#         log_data = {
#             'Name': record.name,
#             'Level': record.levelname,
#             'Message': record.getMessage(),
#             'TimeStamp': datetime.fromtimestamp(record.created)
#         }
#         self.buffer.append(log_data)

#         if len(self.buffer) >= self.BATCH_SIZE:
#             self.flush()

#     def flush(self):
#         if self.buffer:
#             self.collection.insert_many(self.buffer)
#             self.buffer = []

#     def close(self):
#         self.flush()
#         super().close()


if __name__ == "__main__":
    # Get a logger in the main script
    custom_logger = EdgeAppLogger(__name__)
    custom_logger.log('Debugging application start', logging.DEBUG)

    # Another log message
    # custom_logger.log('This is a warning from the main script', logging.WARNING, log_to_mongodb=True)
