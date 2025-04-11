from abc import ABCMeta
import threading
import yaml

class Singleton(metaclass=ABCMeta):
    '''
    an abstract class to keep only one instance at runtime.
    
    * attrs:
    _instance: an internal attr to keep created instance and checka only one is created
    _lock: an threading lock to ensure only one thread is holding the lock and evaluating instance
     
    * response data format
    cls._instance: return the exist / first instance
    
    '''
    _instance = None
    _lock = threading.Lock()
    # 2023-09-05 Eric: add *args to receive child params but won't be used
    # ! it's used to avoid __new__ only takes 1 argument but more were given error
    # ! use *args as tuple; otherwise if applys **kwargs as dict then a param name needs to specify
    def __new__(cls, *args):
        if cls._instance is None:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

class PropertyDefinition:
    def __init__(self, name: str, type: any, value: any) -> None:
        self.name = name
        self.type = type
        self.value = value

def load_yaml(file_name: str, property_name: str):
    '''
    load property values from config.yaml

    2023-07-12 Eric:
    暫不使用try-cache / default value處理:
    人為缺失不應使用上述機制防呆, 確保部屬期間可及早注意關鍵字等缺失

    2023-04-28 Eric: 
    CWD會依執行程式的目錄改變, 會影響相對路徑的正確性, 
    需使用下列程式碼取得當前路徑後組成絕對路徑來使用
    import os
    dir = os.path.dirname(__file__)
    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        # loader = yaml.FullLoader
        # content = yaml.load(file.read(), Loader=loader)
        content = yaml.safe_load(file)
        return content[property_name]

def print_msg(msg: str):
    '''
    print message with distinct format
    '''
    print('\n{} {} {}\n'.format(('*' * 10), msg, ('*' * 10)))
