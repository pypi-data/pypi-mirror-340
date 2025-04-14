from typing import Any, Dict, Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class PriorityLevelWithMaxLamports(BaseModel):
    priority_level: Optional[str] = None
    max_lamports: Optional[int] = None


class PrioritizationFeeLamports(BaseModel):
    priority_level_with_max_lamports: Optional[
        PriorityLevelWithMaxLamports
    ] = None
    jito_tip_lamports: Optional[int] = None


class SwapRequest(BaseModel):
    user_public_key: str
    quote_response: Dict[str, Any]

    wrap_and_unwrap_sol: Optional[bool] = None
    use_shared_accounts: Optional[bool] = None
    fee_account: Optional[str] = None
    tracking_account: Optional[str] = None
    prioritization_fee_lamports: Optional[PrioritizationFeeLamports] = None
    as_legacy_transaction: Optional[bool] = None
    destination_token_account: Optional[str] = None
    dynamic_compute_unit_limit: Optional[bool] = None
    skip_user_accounts_rpc_calls: Optional[bool] = None
    dynamic_slippage: Optional[bool] = None
    compute_unit_price_micro_lamports: Optional[int] = None
    blockhash_slots_to_expiry: Optional[int] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True

    def to_dict(self) -> Dict[str, Any]:
        params = self.model_dump(exclude_none=True)

        camel_case_params = {
            to_camel(key): value for key, value in params.items()
        }

        return camel_case_params
