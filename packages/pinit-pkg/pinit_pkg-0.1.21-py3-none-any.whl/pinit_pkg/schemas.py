from pydantic import BaseModel, Field


class ClusterHeaders(BaseModel):
    content_type: str = Field(..., pattern='^application/json$', alias='content-type')


class AuthHeaders(BaseModel):
    authorization: str = Field(..., pattern='^Bearer .+$', alias='Authorization')
