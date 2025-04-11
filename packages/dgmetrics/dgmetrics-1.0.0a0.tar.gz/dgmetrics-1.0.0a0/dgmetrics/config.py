from typing import Dict, Optional, List
from pydantic import BaseModel, field_validator, conint
import re

class TriggerConfig(BaseModel):
    trigger_count: conint(ge=0)  # целое число >= 0
    trigger_time: str  # строка с временным интервалом

    @classmethod
    @field_validator('trigger_time')
    def validate_trigger_time(cls, v: str) -> str:
        if not re.fullmatch(r'^\d+[mhd]$', v):
            raise ValueError('trigger_time must be in format <number>m, <number>h or <number>d')
        return v

class MetricConfig(BaseModel):
    name: str
    documentation: str
    labels: Optional[Dict[str, TriggerConfig]] = None  # опциональный словарь с произвольными ключами

class MetricListConfig(BaseModel):
    __root__: List[MetricConfig]  # корневой список конфигураций
