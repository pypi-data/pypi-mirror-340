from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
import time

from shared.base.config import MongoDBSettings

DEFAULT_TIMEFIELD = 'TimeStamp'
DEFAULT_METAFIELD = 'Meta'
DEFAULT_GRANU = 'seconds'
DEFAULT_EXPIRE_TIME = 691200  # 8 days


class MongoDBConnection:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, **kwargs):

        self.host = kwargs.get("host", MongoDBSettings.HOST)
        self.port = kwargs.get("port", int(MongoDBSettings.PORT))
        self.username = kwargs.get("username", MongoDBSettings.USERNAME)
        self.password = kwargs.get("password", MongoDBSettings.PASSWORD)
        self.authSource = kwargs.get("authSource", MongoDBSettings.AUTH_SOURCE)
        self.maxPoolSize = kwargs.get("maxPoolSize", MongoDBSettings.MAX_POOL_SIZE)

        if not hasattr(self, 'client'):
            self._connect()

    def _connect(self):
        """Initialize the MongoDB client with native retry configurations."""
        try_cnt = 0
        while True:
            try_cnt += 1
            try:
                self.client = MongoClient(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    authSource=self.authSource,
                    maxPoolSize=self.maxPoolSize,
                    socketTimeoutMS=10000,              # 10 seconds for socket operations
                    serverSelectionTimeoutMS=10000,     # 10 seconds to select a server
                    retryWrites=True,                   # Enable automatic retries for write operations
                    retryReads=True,                    # Enable automatic retries for read operations
                    heartbeatFrequencyMS=10000          # 10 seconds for heartbeat checks
                )
                # Test the connection
                self._ensure_connection()
                break
            except:
                self.client = None
                print(f"{datetime.utcnow()} *** Cannot init MongoDB connection... Keep trying: {try_cnt}")
                time.sleep(10)

        print(f"{datetime.utcnow()} Connect to mongo db successfully.")
        print('=' * 60)

    def _ensure_connection(self):
        """Ensure the MongoDB connection is alive."""
        try:
            result = self.client.admin.command('ping')
            print(f"MongoDB connection result: {result}")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"MongoDB connection issue detected: {e}")
            raise 

    def _retry_operation(self, operation, *args, **kwargs):
        """Wrapper to retry a database operation if needed."""
        try:
            self._ensure_connection()
            return operation(*args, **kwargs)
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Operation failed due to connection issue: {e}")
            self._connect()
            print("Retrying operation after re-establishing connection...")
            return operation(*args, **kwargs)

    def list_database_names(self):
        return self.client.list_database_names()

    def get_database(self, db_name):
        return self._retry_operation(lambda: self.client[db_name])

    def get_collection(self, db, col_name):
        return db[col_name]

    def insert_one(self, database_name, collection_name, doc:dict={}):
        db = self.get_database(database_name)
        db[collection_name].insert_one(doc)

    def insert_many(self, database_name, collection_name, docs:list=[], ordered=True):
        db = self.get_database(database_name)
        db[collection_name].insert_many(docs, ordered=ordered)

    def collection_exists(self, database_name, collection_name):
        db = self.get_database(database_name)
        return collection_name in db.list_collection_names()

    def init_time_series_collection(self, database_name: str, collection_name: str, collection_meta: dict):
        """Initialize or update a time-series collection with specified metadata."""
        db = self.get_database(database_name)

        # Check if the collection exists
        if not self.collection_exists(database_name, collection_name):
            self._create_collection(db, database_name, collection_name, collection_meta)
        else:
            print(f"Collection <'{collection_name}'> already exists.")
            self._verify_and_update_collection(db, database_name, collection_name, collection_meta)
        
        # Add indexes
        indexes = collection_meta.get('Indexes', [])
        for index in indexes:
            self._create_index(db, collection_name, index)

        print(f"Initialization of collection <'{collection_name}'> completed successfully.")
        print('=' * 60)

    def _create_collection(self, db, database_name:str, collection_name: str, collection_meta: dict):
        """Create a new time-series collection with the specified metadata."""
        try:
            db.create_collection(
                collection_name,
                timeseries={
                    'timeField': collection_meta.get('TimeField', DEFAULT_TIMEFIELD),
                    'metaField': collection_meta.get('MetaField', DEFAULT_METAFIELD),
                    'granularity': collection_meta.get('Granularity', DEFAULT_GRANU)
                },
                expireAfterSeconds=collection_meta.get('ExpireAfterSeconds', DEFAULT_EXPIRE_TIME)
            )
            print(f"Created collection <'{collection_name}'> successfully.")
        except Exception as e:
            print(f"Error creating collection <'{collection_name}'>: {e}")

    def _verify_and_update_collection(self, db, database_name:str, collection_name: str, collection_meta: dict):
        """Verify collection metadata and recreate the collection if configurations differ."""
        try:
            collection_info = db.command("listCollections", filter={"name": collection_name})
            options: dict = collection_info['cursor']['firstBatch'][0].get("options", {})
            timeseries_info: dict = options.get('timeseries', {})
            expire_time = options.get('expireAfterSeconds', 0)

            # Extract current metadata
            old_time_field = timeseries_info.get("timeField")
            old_meta_field = timeseries_info.get("metaField")
            old_granularity = timeseries_info.get("granularity")

            # Check for mismatches
            if any([
                old_time_field != collection_meta.get('TimeField', DEFAULT_TIMEFIELD),
                old_meta_field != collection_meta.get('MetaField', DEFAULT_METAFIELD),
                old_granularity != collection_meta.get('Granularity', DEFAULT_GRANU),
                expire_time != collection_meta.get('ExpireAfterSeconds', DEFAULT_EXPIRE_TIME)
            ]):
                print(f"Collection <'{collection_name}'> configuration mismatch. Recreating...")
                print(f"Current Config: ({old_time_field}, {expire_time}, {old_meta_field}, {old_granularity})")
                print(f"New Config: ({collection_meta.get('TimeField', DEFAULT_TIMEFIELD)}, {collection_meta.get('ExpireAfterSeconds', DEFAULT_EXPIRE_TIME)}, {collection_meta.get('MetaField', DEFAULT_METAFIELD)}, {collection_meta.get('Granularity', DEFAULT_GRANU)})")
                self.recreate_time_series_collection(database_name, collection_name, collection_meta)
        except Exception as e:
            print(f"Failed to verify collection <'{collection_name}'>: {e}")

    def _create_index(self, db, collection_name: str, index: dict):
        """Create an index on the collection."""
        try:
            db[collection_name].create_index(index)
            print(f"Index created: {index}")
        except Exception as e:
            print(f"Error creating index {index} on collection <'{collection_name}'>: {e}")

    def recreate_time_series_collection(self, database_name, origin_collection_name, collection_meta, batch_size=1000):
        """
        Recreate a time-series collection with updated metadata.

        Args:
            database_name (str): Name of the database.
            origin_collection_name (str): Name of the original collection.
            collection_meta (dict): Metadata for the new collection.
            batch_size (int): Number of documents to move per batch.
        """
        new_field_name = collection_meta.get('TimeField', DEFAULT_TIMEFIELD)
        db = self.get_database(database_name)
        original_collection = db[origin_collection_name]

        # Check if the collection exists and is a time-series collection
        if origin_collection_name in db.list_collection_names():
            try:
                collection_info = db.command("listCollections", filter={"name": origin_collection_name})
                options: dict = collection_info['cursor']['firstBatch'][0].get("options", {})
                timeseries_info: dict = options.get('timeseries', {})
                old_field_name = timeseries_info.get("timeField")
                is_time_series = old_field_name is not None

                if not is_time_series:
                    print(f"The collection '{origin_collection_name}' is not a time-series collection.")

                # Create a temporary collection
                temp_collection_name = f"{origin_collection_name}_temp"
                if temp_collection_name in db.list_collection_names():
                    db[temp_collection_name].drop()

                db.create_collection(
                    temp_collection_name,
                    timeseries={
                        'timeField': new_field_name,
                        'metaField': collection_meta.get('MetaField', DEFAULT_METAFIELD),
                        'granularity': collection_meta.get('Granularity', DEFAULT_GRANU)
                    },
                    expireAfterSeconds=collection_meta.get('ExpireAfterSeconds', DEFAULT_EXPIRE_TIME)
                )
                temp_collection = db[temp_collection_name]
                print(f"Temporary collection '{temp_collection_name}' created successfully.")

                # Copy documents to the temporary collection with updated time field
                self._migrate_documents(
                    source_collection=original_collection,
                    target_collection=temp_collection,
                    old_field_name=old_field_name,
                    new_field_name=new_field_name,
                    batch_size=batch_size
                )

                # Drop the original collection
                original_collection.drop()
                print(f"Dropped original collection '{origin_collection_name}'.")

                # Recreate the original collection with the updated time field
                db.create_collection(
                    origin_collection_name,
                    timeseries={
                        'timeField': new_field_name,
                        'metaField': collection_meta.get('MetaField', DEFAULT_METAFIELD),
                        'granularity': collection_meta.get('Granularity', DEFAULT_GRANU)
                    },
                    expireAfterSeconds=collection_meta.get('ExpireAfterSeconds', DEFAULT_EXPIRE_TIME)
                )
                original_collection = db[origin_collection_name]

                # Copy documents back from the temporary collection
                self._migrate_documents(
                    source_collection=temp_collection,
                    target_collection=original_collection,
                    batch_size=batch_size
                )

                # Drop the temporary collection
                temp_collection.drop()
                print(f"Dropped temporary collection '{temp_collection_name}'.")
                print(f"Successfully recreated time-series collection '{origin_collection_name}' with updated time field.")

            except Exception as e:
                print(f"Failed to recreate collection '{origin_collection_name}': {e}")
        else:
            print(f"The collection '{origin_collection_name}' does not exist in the database '{database_name}'.")

    def _migrate_documents(self, source_collection, target_collection, old_field_name=None, new_field_name=None, batch_size=1000):
        """
        Migrate documents from one collection to another, with optional field transformation.

        Args:
            source_collection: The source MongoDB collection.
            target_collection: The target MongoDB collection.
            old_field_name (str, optional): Old time field name in the source collection.
            new_field_name (str, optional): New time field name in the target collection.
            batch_size (int): Number of documents to move per batch.
        """
        pipeline = []
        if old_field_name and new_field_name:
            pipeline.append({"$addFields": {new_field_name: f"${old_field_name}"}})
            if new_field_name != old_field_name:
                pipeline.append({"$project": {old_field_name: 0}})
        
        try:
            documents = source_collection.aggregate(pipeline)
            batch = []
            total_count = 0

            for doc in documents:
                batch.append(doc)
                if len(batch) >= batch_size:
                    target_collection.insert_many(batch, ordered=False)
                    total_count += len(batch)
                    batch = []

            if batch:
                target_collection.insert_many(batch, ordered=False)
                total_count += len(batch)

            print(f"Moved {total_count} documents from '{source_collection.name}' to '{target_collection.name}'.")
        except Exception as e:
            print(f"Failed to migrate documents from '{source_collection.name}' to '{target_collection.name}': {e}")


# Long-Term Connection Instance
mongo_service = MongoDBConnection()


if __name__ == "__main__":
    time_field = "TimeStamp"
    col_meta = {
        "TimeField": time_field,
        "MetaField": "Meta",
        "Indexes": [
            [(time_field, 1)],
            [("Meta.DeviceID", 1)],
            [("Meta.MessageName", 1)],
            [("Meta.DeviceID", 1), (time_field, 1)],
        ],
        "Granularity": "seconds",
        "ExpireAfterSeconds": 10,
    }
    mongo_service.init_time_series_collection('test-mogo-ts', 'test', collection_meta=col_meta)
