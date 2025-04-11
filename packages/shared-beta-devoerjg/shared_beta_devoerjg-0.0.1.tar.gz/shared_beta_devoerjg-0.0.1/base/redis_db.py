# redis_db.py
# redis connection 

import time
import redis

from shared.base.config import RedisSettings


class RedisConnection:
    def __init__(self, max_retry=10000, retry_interval=10) -> None:
        self.connection_pool: redis.ConnectionPool = None
        self.db: redis.StrictRedis = None
        self.pubsub: redis.client.PubSub = None

        self.max_retries = max_retry
        self.retry_interval = retry_interval

        self._connect()

    def _connect(self):
        retry_cnt = 0
        while retry_cnt < self.max_retries:
            try:
                self.connection_pool = redis.ConnectionPool(
                    host=RedisSettings.HOST,
                    port=RedisSettings.PORT,
                    password=RedisSettings.PASSWORD,
                    decode_responses=True,
                    max_connections=RedisSettings.REDIS_POOL_SIZE,  # Adjust the max number of connections as needed
                    socket_keepalive=True                           # Send TCP pack for keep socket alive
                )
                self.db = redis.StrictRedis(connection_pool=self.connection_pool)
                self.pubsub = self.db.pubsub(ignore_subscribe_messages = True)
                self.db.ping()
                print("Redis connection established.")
                return
            except redis.ConnectionError as e:
                print(f"Redis connection failed: {e}. Retry: {retry_cnt}/{self.max_retries} in {self.retry_interval} secs...")
                retry_cnt += 1
                time.sleep(self.retry_interval)

        raise redis.ConnectionError(f'Failed to connect to Redis after {self.max_retries} retries...') # ! GIVE UP

    def _ensure_connection(self):
        """Ensure the Redis connection is alive."""
        try:
            self.db.ping()
        except redis.ConnectionError as e:
            print(f"Redis connection issue detected: {e}")
            raise

    def _retry_operation(self, operation, *args, **kwargs):
        """Wrapper to retry a database operation if needed."""
        try:
            self._ensure_connection()
            return operation(*args, **kwargs)
        except redis.ConnectionError as e:
            print(f"Operation failed due to connection issue: {e}")
            self._connect()
            print("Retrying operation after re-establishing connection...")
            return operation(*args, **kwargs)

    def expire(self, name, time:int=1):
        self.db.expire(name=name, time=time)

    def publish_message(self, channel_name:str, message:dict):
        '''
        Redis method to broadcast a message 
        '''
        self._retry_operation(lambda: self.db.publish(channel=channel_name, message=message))

    def subscribe_to_channel(self, channel_name: str):
        """
        Subscribe to a channel to receive messages.
        """
        self._retry_operation(lambda: self.pubsub.subscribe(channel_name))

    def get_next_message(self):
        """
        Get the next message from the subscribed channel.
        """
        messages = self.pubsub.get_message()
        return messages

    def init_value(self, name:str, init_value:str|float|int, re_init:bool=True):
        def operation():
            if re_init or not self.db.exists(name):
                self.db.delete(name)
                if init_value:
                    self.db.set(name=name, value=init_value)
            else:
                print(f"Redis - {name} already exists")
        self._retry_operation(operation)

    def init_list(self, name:str, init_value:list=list(), re_init:bool=False):
        def operation():
            if re_init or not self.db.exists(name):
                self.db.delete(name)
                if init_value:
                    self.db.rpush(name, *init_value)
            else:
                print(f"Redis - {name} already exists")
        self._retry_operation(operation)

    def init_hash(self, name:str, init_value:dict|None=None, re_init:bool=False):
        def operation():
            if re_init or not self.db.exists(name):
                self.db.delete(name)
                if init_value:
                    self.db.hset(name, mapping=init_value)
                print(f"Redis Initialized - {name}")
            else:
                print(f"Redis - {name} already exists")
        self._retry_operation(operation)

    def init_set(self, name:str, init_value:set|None=None, re_init:bool=False):
        def operation():
            if re_init or not self.db.exists(name):
                self.db.delete(name)
                if init_value:
                    self.db.sadd(name, *init_value)
                print(f"Redis Initialized - {name}")
            else:
                print(f"Redis - {name} already exists")
        self._retry_operation(operation)

    def get_value(self, name:str, type_func=None):
        '''
        Retrieve the value from the simple redis key-value pair
        '''
        def operation():
            result = self.db.get(name=name)
            if result and type_func:
                result = type_func(result)
        
            return result
        return self._retry_operation(operation)

    def get_keys(self, pattern):
        return self._retry_operation(lambda: redis_service.db.keys(pattern=pattern))

    def get_set(self, name:str):
        return self._retry_operation(lambda: set(self.db.smembers(name=name)))

    def get_list(self, name:str, start:int=0, end:int=-1):
        def operation():
            l = self.db.lrange(name=name, start=start, end=end)
            l = list(l) if l else list()
            return l
        return self._retry_operation(operation)

    def get_list_item(self, name:str, index:int) -> None:
        return self._retry_operation(lambda: self.db.lindex(name, index=index))
    
    def add_items_to_list(self, name:str, item:list) -> None:
        """
        Append a list to redis list with the given list name
        """
        self._retry_operation(lambda: self.db.rpush(name, *item))

    def add_items_to_set(self, name:str, *items) -> None:
        """
        Add an item to the existing redis set
        """
        def operation():
            if len(items) == 1:
                self.db.sadd(name, items[0])
            else:
                self.db.sadd(name, *items)
        self._retry_operation(operation)

    def get_hash_dict(self, name:str):
        return self._retry_operation(lambda: self.db.hgetall(name))

    def get_hash_value(self, name:str, key:str, type_func=None, **kwargs):
        """
        Get value from the redis hash with given hash name and field key.

        ### Args:
        #### Args: `type_func`
        type transforming function (e.g. int, float, str.)
        """
        def operation():
            if not type_func:
                return self.db.hget(name, key)
            else:
                result = self.db.hget(name, key)
                if result:
                    result = type_func(result, **kwargs) if kwargs else type_func(result)
                return result
        return self._retry_operation(operation)
    
    def increment_hash_value(self, name:str, key:str, increment_value:int|float) -> None:
        self._retry_operation(lambda: self.db.hincrbyfloat(name, key, increment_value))

    def update_hash(self, name, update_dict:dict):
        def operation():
            if not update_dict:
                return
            self.db.hset(name, mapping=update_dict)
        return self._retry_operation(operation)

    def query_hashes_keys(self, prefix: str, query_dict: dict | None = None) -> dict:
        '''
        Query Redis hashes' keys with given prefix and dict.

        ### Args
        #### Args: `prefix`
        For example, to query all hashes such as `device-status:d1` `device-status:d2` `device-status:d3`,
        use `prefix='device-status'` for querying.

        #### Args: `query_dict`
        For example, to query out hashes with fields 
        (i.e. querying with case matching)
        '''
        def operation():
            print(f"\nRedis Query for {prefix}")
            start_time = time.time()

            # Retrieve all keys for the given prefix
            redis_keys = self.db.keys(pattern=f'{prefix}:*')
            redis_keys = set(redis_keys)

            time.sleep(2)
            # Query with conditions
            if query_dict:
                # Create indexes for fields using a pipeline
                with self.db.pipeline() as pipe:
                    for key in redis_keys:
                        for field, value in query_dict.items():
                            query_value = self.db.hget(key, field)
                            if str(value) == query_value:
                                pipe.sadd(f'index:{field}:{value}', key)
                    pipe.execute()  # Execute pipeline commands

                # Query using secondary indexes
                for field, value in query_dict.items():
                    index_name = f'index:{field}:{value}'
                    query_result = self.db.smembers(index_name)
                    redis_keys = redis_keys.intersection(query_result)
                    
                    # Clear index_name after used
                    redis_service.db.delete(index_name)

            execution_time_redis = time.time() - start_time
            print("Query Execution Time (Redis):", execution_time_redis)
            return redis_keys
        return self._retry_operation(operation)

# Long-Term Connection Instance
redis_service = RedisConnection()


if __name__ == "__main__":

    # A Basic hash structure implement
    redis_service.db.delete("test-dict")
    test_dict = {"name": "John", "surname": "Smith", "company": "Redis", "age": '29'}
    redis_service.db.hset( # original redis pck
        "test-dict",
        mapping=test_dict,
    )
    time.sleep(30)
    print(redis_service.get_hash_dict("test-dict") == test_dict)
    print(redis_service.db.hgetall("test-dict") == test_dict)

    # Test Hash self-defined method
    redis_service.init_hash(name="test-dict", init_value=test_dict, re_init=True)
    print(redis_service.db.hgetall("test-dict") == test_dict)

    # Initialize the key-value pair with an integer value
    initial_value = 5  # Change this to the desired initial value
    redis_service.db.delete("test")
    redis_service.db.hset("test", "key", initial_value)

    # Increment the field by 10
    result = redis_service.db.hincrby("test", "key", 10)
    print("Result:", result)
    redis_service.db.delete("test-dict")
    redis_service.db.delete("test")

    # Test for querying
    test_dict_1 = {"name": "John", "surname": "A", "company": "Redis", "age": '29'}
    test_dict_2 = {"name": "Tom", "surname": "B", "company": "Redis", "age": '45'}
    test_dict_3 = {"name": "Bob", "surname": "A", "company": "Goog", "age": '30'}
    redis_service.init_hash(name="test:test-dict:1", init_value=test_dict_1, re_init=True)
    redis_service.init_hash(name="test:test-dict:2", init_value=test_dict_2, re_init=True)
    redis_service.init_hash(name="test:test-dict:3", init_value=test_dict_3, re_init=True)
    redis_service.init_hash(name="test:hello-world", init_value=test_dict_3, re_init=True)

    result = redis_service.query_hashes(prefix="test-dict")
    print(result)
    result = redis_service.query_hashes(prefix="test-dict", query_dict={})
    print(result)
    result = redis_service.query_hashes(prefix="test-dict", query_dict={"company": "Redis", "surname": None})
    print(result)

    # Test for lists
    redis_service.init_list('test-list')
    redis_service.expire('test-list')
    redis_service.init_list('test-list', ['a', 'b', 'c'])

    # Test for empty hash
    redis_service.init_hash('test-empty', init_value={}, re_init=True)
    redis_service.expire('test-empty')
    redis_service.init_hash('test-empty', re_init=True)

    # Test for increment
    redis_service.init_hash('test-incre', init_value={'int_field': 100, 'float_field':100.1000}, re_init=True)
    redis_service.expire('test-incre')
    redis_service.increment_hash_value('test-incre', 'int_field', 10)
    redis_service.increment_hash_value('test-incre', 'float_field', -10.134)
    print(redis_service.get_hash_dict('test-incre'))
