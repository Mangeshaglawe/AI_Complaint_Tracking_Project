from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ComplaintData(BaseModel):
    model_config = ConfigDict(extra="allow")

    customer_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    complaint_category: Optional[str] = None
    issue_description: Optional[str] = None
    resolution_provided: Optional[str] = None
    is_complaint: bool = False
    escalation_required: bool = False
    supporting_document: bool = False
    overall_status: Optional[str] = None
