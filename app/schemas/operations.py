from pydantic import BaseModel, Field


# Model pentru PUTERE
class PowerRequest(BaseModel):
    base: int = Field(..., description="The base number")
    exponent: int = Field(..., description="The exponent")


class PowerResponse(BaseModel):
    result: int


# Model pentru FACTORIAL
class FactorialRequest(BaseModel):
    number: int = Field(..., ge=0, description="A non-negative number")


class FactorialResponse(BaseModel):
    result: int


# Model pentru FIBONACCI
class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0, description="Fibonacci index")


class FibonacciResponse(BaseModel):
    result: int
