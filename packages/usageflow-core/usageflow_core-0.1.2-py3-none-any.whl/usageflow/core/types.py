from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class ApiConfigStrategy:
    id: str  # Assuming ObjectId can be represented as a string
    name: str
    account_id: str
    identity_field_name: str
    identity_field_location: str
    config_data: Dict[str, Any]
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = field(default=None)
    application_id: Optional[str] = field(default=None)

@dataclass
class Policy:
    policy_id: str = field(metadata={"json": "policyId"})
    account_id: str = field(metadata={"json": "accountId"})
    application_id: str = field(metadata={"json": "applicationId"})
    endpoint_pattern: str = field(metadata={"json": "endpointPattern"})
    endpoint_method: str = field(metadata={"json": "endpointMethod"})
    identity_field: str = field(metadata={"json": "identityField"})
    identity_location: str = field(metadata={"json": "identityLocation"})
    rate_limit: int = field(metadata={"json": "rateLimit"})
    rate_limit_interval: str = field(metadata={"json": "rateLimitInterval"})
    metering_expression: str = field(metadata={"json": "meteringExpression"})
    metering_trigger: str = field(metadata={"json": "meteringTrigger"})
    stripe_price_id: str = field(metadata={"json": "stripePriceId"})
    stripe_customer_id: str = field(metadata={"json": "stripeCustomerId"})
    created_at: int = field(metadata={"json": "createdAt"})
    updated_at: int = field(metadata={"json": "updatedAt"})
    # ledger_id: Optional[str] = field(default=None, metadata={"json": "ledgerId"})  # Uncomment if needed
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Policy":
        """Convert camelCase JSON keys to snake_case dataclass fields"""
        field_map = {f.metadata["json"]: name for name, f in cls.__dataclass_fields__.items()}
        transformed_data = {field_map[k]: v for k, v in data.items() if k in field_map}
        return cls(**transformed_data)
