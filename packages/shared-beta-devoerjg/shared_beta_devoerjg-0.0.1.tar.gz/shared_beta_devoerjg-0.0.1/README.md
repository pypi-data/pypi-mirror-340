## Project Name
Edge-Shared

## Description
Edge-Shared is a fundamental module project stored in an individual repo, it defines some basic classes and common functions for other edge service projects to import.

### Import Process
1. add `shared/` at `.gitignore` file in your project
2. clone edge-shared repo into your project and rename it as `shared`
3. now you can import all the class and methods without affecting your project repo

### Development Process

1. develop your common classes or methods in a proper path
2. import your new modules, classes, or methods into `__init__.py`
3. update the Project Structure at  `README.md`

## Project Structure

```
shared/
├── base/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api_log.py
│   │   └── api.py
│   │
│   ├── __init__.py
│   ├── common.py
│   ├── config.py
│   ├── device.py
│   ├── message.py
│   └── mqtt.py
│ 
├── protocol_sdk/
│   ├── common/
│   │   ├── __init__.py
│   │   ├── struct_dcfx.py
│   │   └── verify.py
│   ├── __init__.py
│   ├── dcfx_sdk.py
│   └── mqtt_sdk
│
├── .gitignore
├── config.yaml
├── README.md
└── requirements.txt
```

## Points to know

1. `protocol_sdk` is maintained by Middleware team. The message topic and payload structure in `dcfx_sdk.py` should be checked to keep it meets the latest version of Delta Connected Factory Exchange Standard.

2. `base/api.py` includes `BaseAPI` to implement an api request with log, param validation, and formatted result data.