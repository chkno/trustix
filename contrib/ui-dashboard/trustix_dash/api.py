import asyncio
from trustix_dash.models import (
    DerivationOutputResult,
    Derivation,
)
from tortoise.query_utils import Q
from typing import (
    Coroutine,
    Dict,
    List,
)


async def get_derivation_outputs(drv: str) -> List[Derivation]:
    async def filter(q_filter):
        qs = (
            Derivation.filter(q_filter)
            .prefetch_related("derivationoutputs")
            .prefetch_related("derivationoutputs__derivationoutputresults")
        )
        return await qs

    coros: List[Coroutine] = [
        filter(q_filter)
        for q_filter in (Q(from_ref_recursive__referrer=drv), Q(drv=drv))
    ]

    items: List[Derivation] = []
    for items_ in await asyncio.gather(*coros):
        items.extend(items_)

    return items


async def get_derivation_output_results_unique(
    *output_hash: bytes,
) -> List[DerivationOutputResult]:
    if not output_hash:
        return []

    results: Dict[bytes, DerivationOutputResult] = {
        result.output_hash: result  # type: ignore
        for result in await DerivationOutputResult.filter(output_hash__in=output_hash)
    }

    if len(results) != len(output_hash):
        raise ValueError(
            "{} ids passed but only returned {} results".format(
                len(output_hash), len(results)
            )
        )

    return [results[h] for h in output_hash]