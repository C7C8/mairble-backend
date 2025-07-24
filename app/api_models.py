import datetime
from typing import Optional, List

from pydantic import BaseModel


class FetchRequest(BaseModel):
    api_key: str  # PriceLabs API key from frontend
    listing_id: Optional[str] = None  # Listing ID from frontend
    pms: Optional[str] = None  # PMS from frontend
    date_from: Optional[str] = None  # yyyy-mm-dd
    date_to: Optional[str] = None


class NightData(BaseModel):
    date: str
    your_price: Optional[float]
    market_avg_price: Optional[float]
    occupancy: Optional[float]
    event: Optional[str]
    day_of_week: Optional[str]
    lead_time: Optional[int]
    # New valuable fields from PriceLabs
    adr_last_year: Optional[float]  # ADR_STLY - historical benchmark
    neighborhood_demand: Optional[str]  # nhood_demand - granular demand level
    min_price_limit: Optional[float]  # minimum_price - pricing floor
    avg_los_last_year: Optional[float]  # avg_los_STLY - historical stay length
    seasonal_profile: Optional[str]  # minstay_seasonal_profile - seasonal context


class LLMResult(BaseModel):
    date: str
    suggested_price: Optional[float]
    confidence: Optional[int]
    explanation: Optional[str]
    insight_tag: Optional[str]


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime


class ConversationInfo(BaseModel):
    conversation_id: str
    created_at: datetime.datetime
    last_message_at: datetime.datetime
    message_count: int
    property_context: Optional[dict] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    property_context: Optional[dict] = None  # Guest profile, competitive advantage, booking patterns


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


class GetConversationRequest(BaseModel):
    conversation_id: str


class GetConversationResponse(BaseModel):
    conversation_id: str
    messages: List[ChatMessage]
    property_context: Optional[dict] = None


class AnalyzeRequest(BaseModel):
    nights: List[NightData]
    model: Optional[str] = "gpt-4"


class SingleOverrideRequest(BaseModel):
    api_key: str
    listing_id: str
    pms: str
    date: str
    price: float
    price_type: str = "fixed"  # Default to fixed
    currency: str = "USD"
    reason: str = "Manual update via mAIrble"
    update_children: bool = False


class SingleOverrideResponse(BaseModel):
    success: bool
    message: str
    updated_date: Optional[str] = None
    error_details: Optional[str] = None
