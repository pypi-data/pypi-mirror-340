from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from jup_ag_sdk.models.common.dex_enum import DexEnum


class QuoteRequest(BaseModel):
    input_mint: str
    output_mint: str
    amount: int
    slippage_bps: Optional[int] = None
    swap_mode: Optional[str] = None
    dexes: Optional[List[DexEnum]] = None
    exclude_dexes: Optional[List[DexEnum]] = None
    restrict_intermediate_tokens: Optional[bool] = None
    only_direct_routes: Optional[bool] = None
    as_legacy_transaction: Optional[bool] = None
    max_accounts: Optional[int] = None
    platform_fee_bps: Optional[int] = None
    dynamic_slippage: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        params = self.model_dump(exclude_none=True)

        camel_case_params = {
            to_camel(key): value for key, value in params.items()
        }

        if "dexes" in camel_case_params:
            camel_case_params["dexes"] = ",".join(
                [str(dex) for dex in camel_case_params["dexes"]]
            )
        if "excludeDexes" in camel_case_params:
            camel_case_params["excludeDexes"] = ",".join(
                [str(dex) for dex in camel_case_params["excludeDexes"]]
            )

        return camel_case_params
