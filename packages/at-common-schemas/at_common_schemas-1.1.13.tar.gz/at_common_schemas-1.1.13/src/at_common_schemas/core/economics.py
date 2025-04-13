from pydantic import Field
from at_common_schemas.base import BaseSchema
from datetime import datetime

class TreasuryRates(BaseSchema):
    date: datetime = Field(..., description="Date of the data")
    month1: float = Field(..., description="1-month Treasury rate")
    month2: float = Field(..., description="2-month Treasury rate")
    month3: float = Field(..., description="3-month Treasury rate")
    month6: float = Field(..., description="6-month Treasury rate")
    year1: float = Field(..., description="1-year Treasury rate")
    year2: float = Field(..., description="2-year Treasury rate")
    year3: float = Field(..., description="3-year Treasury rate")
    year5: float = Field(..., description="5-year Treasury rate")
    year7: float = Field(..., description="7-year Treasury rate")
    year10: float = Field(..., description="10-year Treasury rate")
    year20: float = Field(..., description="20-year Treasury rate")
    year30: float = Field(..., description="30-year Treasury rate")
    
class Indicators(BaseSchema):
    name: str = Field(..., description="Name of the indicator")
    value: float = Field(..., description="Value of the indicator")
    date: datetime = Field(..., description="Date of the data")