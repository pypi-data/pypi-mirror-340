from pydantic import Field
from at_common_schemas.base import BaseSchema

class AbstractEntry(BaseSchema):
    name: str = Field(..., description="name of the entry")

class Index(AbstractEntry):
    symbol: str = Field(..., description="Index symbol")

class Stock(AbstractEntry):
    symbol: str = Field(..., description="Stock symbol")

class Exchange(AbstractEntry):
    pass

class Sector(AbstractEntry):
    pass

class Industry(AbstractEntry):
    pass

class Country(AbstractEntry):
    pass