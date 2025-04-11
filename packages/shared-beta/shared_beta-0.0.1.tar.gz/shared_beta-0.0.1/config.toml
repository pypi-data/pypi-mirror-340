from dataclasses import dataclass
import os

from tools.node_info import get_node_ip

'''
config data-classes define properties for developers to retrieve
all values are loaded from config.yaml
'''

@dataclass
class MongoDBSettings:
    HOST: str = os.environ.get('MONGODB_HOST', '10.146.212.85')
    PORT: int = int(os.environ.get('MONGODB_PORT', 31499))
    USERNAME: str = os.environ.get('MONGODB_USERNAME', 'admin')
    PASSWORD: str = os.environ.get('MONGODB_PASSWORD', 'deltaEdgeService#2023')
    AUTH_SOURCE: str = os.environ.get('MONGODB_AUTH_SOURCE', 'admin')
    MAX_POOL_SIZE: int = int(os.environ.get('MONGODB_MAX_POOL_SIZE', 100))


@dataclass
class MQTTSettings:
    HOST: str = os.environ.get('MQTT_BROKER_HOST', '10.146.212.85') # ! removed 


@dataclass
class ServiceEnvSettings:
    SERVICE_MODE: str = os.environ.get('SERVICE_MODE', 'dev')       # ! removed 
    SERVICE_SCOPE: str = os.environ.get('SERVICE_SCOPE', 'DG3')     # ! removed 
    SERVICE_HOST: str = os.environ.get('HOST', '10.146.212.85')     # ! removed
    TIMEZONE: str = os.environ.get('TZ', 'Asia/Shanghai')
    TIME_SHIFT: str = os.environ.get('TIME_SHIFT', '+0800')         # ! removed 


@dataclass
class RedisSettings:
    HOST: str = os.environ.get('REDIS_HOST', '10.146.212.85')
    PORT: int = int(os.environ.get('REDIS_PORT', 30047))
    PASSWORD: str = os.environ.get('REDIS_PASSWORD', 'iiot@delta2024')
    REDIS_POOL_SIZE: int =  int(os.environ.get('REDIS_POOL_SIZE', 300))


@dataclass
class PostgresSettings:
    HOST: str = os.environ.get('POSTGRES_HOST', '10.147.14.255')
    PORT: int = int(os.environ.get('POSTGRES_PORT', 30225))
    USER: str = os.environ.get('POSTGRES_USER', 'postgres')
    PASSWORD: str = os.environ.get('POSTGRES_PASSWORD', 'postgre@Delta')
    DB: str = os.environ.get('POSTGRES_DB', 'etl')


@dataclass
class AMQPSettings:
    HOST: str = os.environ.get('AMQP_BROKER_HOST', '10.146.212.85')
    PORT: int = int(os.environ.get('AMQP_BROKER_PORT', 30025))
    USER: str = os.environ.get('AMQP_USERNAME', 'guest')
    PASSWORD: str = os.environ.get('AMQP_PASSWORD', 'guest')
    AMQP_QUEUE: str = os.environ.get('AMQP_QUEUE', 'sie-device-info')
    AMQP_EXCHANGE: str = os.environ.get('AMQP_EXCHANGE', 'message-bus')
    AMQP_ROUTING_KEY: str = os.environ.get('AMQP_ROUTING_KEY', default=list)
    AMQP_EXCHANGE_TYPE: str = os.environ.get('AMQP_EXCHANGE_TYPE', 'topic')
    AQMP_TTL: int = int(os.environ.get('AQMP_TTL', 21600000))


@dataclass
class InfluxSettings:
    URL: str = os.environ.get('INFLUXDB_URL', "http://10.147.14.255:30016") # ! removed 
    TOKEN: str = os.environ.get('INFLUXDB_TOKEN', "delta")                  # ! removed 
    ORG: str = os.environ.get('INFLUXDB_ORG', "delta")                      # ! removed 
    BUCKET: str = os.environ.get('INFLUXDB_BUCKET', "edge")                 # ! removed 
    MEASUREMENT: str = os.environ.get('INFLUXDB_MEASUREMENT', "pqm")        # ! removed 


@dataclass
class FlasggerConfig:

    # Test on Local or Deployed Env
    IS_DEPLOYED = os.environ.get("FLASGGER_IS_DEPLOYED", "0")

    # Connection
    API_URL_PREFIX = os.environ.get("API_URL_PREFIX", "sie-edge-api")
    FLASGGER_URL_PREFIX = os.environ.get("FLASGGER_URL_PREFIX", "sie-edge-api-flasgger")
    FLASGGER_STATIC_URL = os.environ.get("FLASGGER_STATIC_URL", "flasgger_static")
    FLASGGER_JSON_ROUTE = os.environ.get("FLASGGER_JSON_ROUTE", "sie-edge-api.json")        # ! removed 

    # Basic UI Information
    TITLE = os.environ.get("FLASGGER_UI_TITLE", "SIE-EDGE-API")
    DESCRIPTION = os.environ.get("FLASGGER_UI_DESCRIPTION", "Edge-API")
    VERSION = os.environ.get("FLASGGER_UI_VERSION", "0.0.1")
    OPERATION_ID = os.environ.get("FLASGGER_OPERATION_ID", "generalAPI")


SWAGGER_CONFIG = {
    # "headers": [],
    "specs": [
        {
            "endpoint": f"{FlasggerConfig.API_URL_PREFIX}",
            "route": f"/{FlasggerConfig.API_URL_PREFIX}.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "swagger_ui": True,
    "static_url_path": f"/{FlasggerConfig.FLASGGER_STATIC_URL}",
    "specs_route": f"/apidocs/",
    "url_prefix": f"/{FlasggerConfig.FLASGGER_URL_PREFIX}",
}


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": f"{FlasggerConfig.TITLE}",
        "description": f"{FlasggerConfig.DESCRIPTION}",
        "version": f"{FlasggerConfig.VERSION}",
    },
    "host": get_node_ip(),
    "basePath": f"/{FlasggerConfig.API_URL_PREFIX}",    # base bash for blueprint registration
    "schemes": ["http", "https"],
    "operationId": f"{FlasggerConfig.OPERATION_ID}",
    # "swaggerUiPrefix": f"/{FlasggerConfig.API_URL_PREFIX}",
}
