from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        use_enum_values=True,
        frozen=False,
        # from_attributes=True,
        # alias_generator=to_pascal,
        json_schema_extra={},
        json_encoders={ObjectId: str, datetime: datetime.isoformat},
        # TODO: json_encoders may be deprecated in future, find alternative solution
        ser_json_timedelta='float',
        validate_default=True,
        protected_namespaces=('_id',),  # avoid conflict with mongo
    )
