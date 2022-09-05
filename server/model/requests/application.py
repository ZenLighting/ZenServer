from datetime import datetime
from typing import Any, Dict, Optional
import pydantic

class StartApplicationRequest(pydantic.BaseModel):
    grid_type: str
    grid_id: str
    
    application_args: Optional[Dict[str, Any]] = {}
    schedule: Optional[datetime] = None
