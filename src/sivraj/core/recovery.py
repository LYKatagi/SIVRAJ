from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from sivraj.log.logger import get_logger

T = TypeVar("T")

logger = get_logger(__name__)


class RecoveryError(Exception):
    """Raised when an operation cannot be recovered."""


class RecoveryManager:
    """
    Executes operations with controlled retries and optional recovery actions.
    """

    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")

        if retry_delay < 0:
            raise ValueError("retry_delay must be >= 0")

        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def run(
        self,
        operation: Callable[[], T],
        *,
        name: str = "operation",
        recover: Callable[[], bool] | None = None,
    ) -> T:
        """
        Execute an operation with retries.

        Args:
            operation:
                Function that performs the operation.

            name:
                Human-readable operation name used in logs.

            recover:
                Optional recovery function. It should return True when
                recovery was successful and False otherwise.

        Returns:
            The result returned by operation().

        Raises:
            RecoveryError:
                If all attempts fail.
        """

        last_error: Exception | None = None

        total_attempts = self.max_retries + 1

        for attempt in range(1, total_attempts + 1):
            logger.info(
                "%s: attempt %d/%d",
                name,
                attempt,
                total_attempts,
            )

            try:
                result = operation()

                logger.info(
                    "%s: operation succeeded",
                    name,
                )

                return result

            except Exception as error:
                last_error = error

                logger.warning(
                    "%s: attempt %d failed: %s",
                    name,
                    attempt,
                    error,
                )

                if attempt >= total_attempts:
                    break

                if recover is not None:
                    logger.info(
                        "%s: attempting recovery",
                        name,
                    )

                    try:
                        recovered = recover()

                    except Exception as recovery_error:
                        logger.error(
                            "%s: recovery failed: %s",
                            name,
                            recovery_error,
                        )
                        recovered = False

                    if recovered:
                        logger.info(
                            "%s: recovery succeeded",
                            name,
                        )
                    else:
                        logger.warning(
                            "%s: recovery did not succeed",
                            name,
                        )

                if self.retry_delay > 0:
                    time.sleep(self.retry_delay)

        logger.critical(
            "%s: all recovery attempts exhausted",
            name,
        )

        raise RecoveryError(f"Unable to recover {name}") from last_error
