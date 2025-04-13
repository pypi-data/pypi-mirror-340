from datetime import datetime
from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.core.economics import TreasuryRates, Indicators

class TreasuryRatesListRequest(BaseSchema):
    from_date: datetime = Field(..., description="Start date for the request")
    to_date: datetime = Field(..., description="End date for the request")

class TreasuryRatesListResponse(BaseSchema):
    items: List[TreasuryRates] = Field(..., description="List of treasury rates")

class IndicatorsListRequest(BaseSchema):
    name: str = Field(..., description="Name of the indicator")

class IndicatorsListResponse(BaseSchema):
    items: List[Indicators] = Field(..., description="List of indicators")