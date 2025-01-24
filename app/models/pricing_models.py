from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ServicePricing:
    service_type: str
    region: str
    price_per_unit: float
    unit_type: str
    
@dataclass
class EC2Instance:
    instance_type: str
    vcpu: int
    memory: float
    price_per_hour: float
    
@dataclass
class CostCalculation:
    service: str
    usage: float
    unit_price: float
    total_cost: float
    details: Optional[Dict] = None 