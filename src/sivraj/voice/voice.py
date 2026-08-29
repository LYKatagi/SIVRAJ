from __future__ import annotations

from typing import Any

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

from sivraj.log.logger import get_logger


logger = get_logger(__name__)


class VoiceError(Exception):
    """Raised when the voice system cannot process audio."""


class Voice:
    """Offline voice input and speech-to-text system."""

    def __init__(
        self,
        *,
        model: str = "base",
        sample_rate: int = 16000,
        channels: int = 1,
    ) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

        logger.info("Loading Whisper model: %s", model)

        try:
            self.model = WhisperModel(
                model,
                device="cpu",
                compute_type="int8",
            )
        except Exception as error:
            logger.exception("Failed to load Whisper model")
            raise VoiceError("Failed to load speech recognition model.") from error

    def get_input(
        self,
        *,
        duration: float = 5.0,
    ) -> np.ndarray:
        """
        Record audio from the default microphone.

        Args:
            duration:
                Recording duration in seconds.

        Returns:
            Recorded audio as a NumPy array.
        """
        if duration <= 0:
            raise ValueError("duration must be greater than 0")

        logger.info(
            "Recording voice input for %.1f seconds",
            duration,
        )

        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
            )

            sd.wait()

        except Exception as error:
            logger.exception("Failed to record audio")
            raise VoiceError("Failed to capture microphone input.") from error

        logger.info("Voice input captured")

        return audio.flatten()

    def parse(self, input_data: Any) -> str:
        """
        Convert recorded audio into text using local Whisper.

        Args:
            input_data:
                Audio returned by get_input().

        Returns:
            Transcribed text.
        """
        if not isinstance(input_data, np.ndarray):
            raise VoiceError("Invalid audio input.")

        if input_data.size == 0:
            raise VoiceError("Audio input is empty.")

        logger.info("Transcribing voice input")

        try:
            segments, _ = self.model.transcribe(
                input_data,
                language="pt",
                beam_size=5,
            )

            text = " ".join(
                segment.text.strip() for segment in segments if segment.text.strip()
            ).strip()

        except Exception as error:
            logger.exception("Failed to transcribe audio")
            raise VoiceError("Failed to transcribe voice input.") from error

        if not text:
            raise VoiceError("No speech detected.")

        logger.info("Voice parsed successfully: %r", text)

        return text
