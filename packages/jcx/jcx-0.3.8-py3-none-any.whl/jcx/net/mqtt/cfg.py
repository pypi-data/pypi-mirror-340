from pydantic import BaseModel


class MqttCfg(BaseModel):
    """MQTT配置"""

    server_url: str
    """服务器URL"""
    root_topic: str
    """根主题"""
