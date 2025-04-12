from typing import Union
import pytest
from equia.models import (
    CalculationComposition, ProblemDetails,
    StatusInput, StatusResult
)
from equia.equia_client import EquiaClient
from utility.shared_settings import sharedsettings

@pytest.mark.asyncio
async def test_call_status():
    client = EquiaClient(sharedsettings.url, sharedsettings.access_key)

    input: StatusInput = client.get_status_input()

    result: Union[StatusResult, ProblemDetails] = await client.call_status_get_async(input)

    await client.cleanup()

    #assert result.status == 400
    assert result.success is True
