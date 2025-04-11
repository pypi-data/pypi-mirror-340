import asyncio
import pytest
from scientist import Experiment

@pytest.mark.asyncio
async def test_experiment_control_vs_candidate():
    exp = Experiment("math_test")

    @exp.control
    def control():
        return 2 + 2

    @exp.candidate
    def candidate():
        return 3 + 2  # Intentional mismatch

    result = await exp.run()
    assert result == 2 + 2  # Control result should be used

@pytest.mark.asyncio
async def test_with_async():
    exp = Experiment("async_test")

    @exp.control
    async def control():
        await asyncio.sleep(0.1)
        return 2 + 2

    @exp.candidate
    async def candidate():
        await asyncio.sleep(0.1)
        return 3 + 2  # Intentional mismatch

    result = await exp.run()
    assert result == 2 + 2  # Control result should be used

@pytest.mark.asyncio
async def test_with_sampling():
    exp = Experiment("sampling_test")
    exp.sample(0.5)  # 50% sampling rate

    @exp.control
    async def control():
        await asyncio.sleep(0.1)
        return 2 + 2

    @exp.candidate
    async def candidate():
        await asyncio.sleep(0.1)
        return 3 + 2  # Intentional mismatch

    result = await exp.run()
    assert result == 2 + 2  # Control result should be used
