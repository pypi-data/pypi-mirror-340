import traceback
import logging
import threading
import asyncio
import time
import random
from typing import Callable, Any, Optional, Union, Awaitable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Observation:
    def __init__(self, name: str, result: Any, duration: float, exception: Optional[Exception] = None):
        self.name = name
        self.result = result
        self.duration = duration
        self.exception = exception

    def has_exception(self):
        return self.exception is not None

class ExperimentResult:
    def __init__(self, control: Observation, candidate: Observation):
        self.control = control
        self.candidate = candidate
        self.match = self.compare()

    def compare(self):
        if self.control.has_exception() or self.candidate.has_exception():
            return False
        return self.control.result == self.candidate.result

class Experiment:
    def __init__(self, name: str):
        self.name = name
        self._control: Optional[Union[Callable, Awaitable]] = None
        self._candidate: Optional[Union[Callable, Awaitable]] = None
        self._enabled = True
        self._comparator: Optional[Callable[[Any, Any], bool]] = None
        self._ignore_exceptions = ()
        self._sample_rate = 1.0  # Default to 100%

    def control(self, func: Callable):
        self._control = func
        return func

    def candidate(self, func: Callable):
        self._candidate = func
        return func

    def compare_with(self, comparator: Callable[[Any, Any], bool]):
        self._comparator = comparator

    def ignore_exceptions(self, *exceptions):
        self._ignore_exceptions = exceptions

    def sample(self, rate: float):
        if not (0.0 <= rate <= 1.0):
            raise ValueError("Sample rate must be between 0.0 and 1.0")
        self._sample_rate = rate

    async def run(self) -> Any:
        if not self._enabled or self._control is None:
            raise RuntimeError("Control function must be defined and experiment enabled")

        control_obs = await self._run_function("control", self._control)

        if self._candidate is not None and random.random() < self._sample_rate:
            asyncio.create_task(self._run_candidate_async(control_obs))

        return control_obs.result

    async def _run_function(self, name: str, func: Union[Callable, Awaitable]) -> Observation:
        start = time.perf_counter()
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
            duration = time.perf_counter() - start
            return Observation(name, result, duration)
        except self._ignore_exceptions as e:
            logger.warning(f"{name} ignored exception: {e}")
            duration = time.perf_counter() - start
            return Observation(name, None, duration, e)
        except Exception as e:
            logger.error(f"{name} unhandled exception: {traceback.format_exc()}")
            duration = time.perf_counter() - start
            return Observation(name, None, duration, e)

    async def _run_candidate_async(self, control_obs: Observation):
        candidate_obs = await self._run_function("candidate", self._candidate)
        result = self._build_result(control_obs, candidate_obs)
        self.publish(result)

    def _build_result(self, control_obs: Observation, candidate_obs: Observation) -> ExperimentResult:
        class CustomResult(ExperimentResult):
            def compare(self):
                if control_obs.has_exception() or candidate_obs.has_exception():
                    return False
                if self._comparator:
                    return self._comparator(control_obs.result, candidate_obs.result)
                return super().compare()
        result = CustomResult(control_obs, candidate_obs)
        result._comparator = self._comparator
        return result

    def publish(self, result: ExperimentResult):
        if not result.match:
            logger.warning(f"[Experiment: {self.name}] Mismatch detected!")
            if result.control.has_exception():
                logger.warning(" - Control exception: %s", result.control.exception)
            else:
                logger.warning(" - Control result: %s", result.control.result)

            if result.candidate.has_exception():
                logger.warning(" - Candidate exception: %s", result.candidate.exception)
            else:
                logger.warning(" - Candidate result: %s", result.candidate.result)

        logger.info(f"[Experiment: {self.name}] Metrics:")
        logger.info(" - Control duration: %.6f sec", result.control.duration)
        logger.info(" - Candidate duration: %.6f sec", result.candidate.duration)
        logger.info(" - Match: %s", result.match)
