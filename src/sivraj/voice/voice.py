
"""SIVRAJ voice input system."""

from __future__ import annotations

import threading
from typing import Any

import numpy as np
import sounddevice as sd
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

        self._recording = False
        self._audio: np.ndarray | None = None
        self._stream: sd.InputStream | None = None
        self._lock = threading.Lock()

        logger.info(
            "Loading Whisper model: %s",
            model,
        )

        try:
            self.model = WhisperModel(
                model,
                device="cpu",
                compute_type="int8",
            )
        except Exception as error:
            logger.exception(
                "Failed to load Whisper model"
            )

            raise VoiceError(
                "Failed to load speech recognition model."
            ) from error

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    @property
    def recording(self) -> bool:
        """Return whether the microphone is currently recording."""

        return self._recording

    def start_recording(self) -> None:
        """Start microphone recording."""

        if self._recording:
            return

        self._audio = None
        self._recording = True

        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                callback=self._audio_callback,
            )

            self._stream.start()

            logger.info("Voice recording started")

        except Exception as error:
            self._recording = False
            self._stream = None

            logger.exception(
                "Failed to start recording"
            )

            raise VoiceError(
                "Failed to start microphone."
            ) from error

    def stop_recording(self) -> np.ndarray:
        """Stop recording and return captured audio."""

        if not self._recording:
            raise VoiceError(
                "Recording is not active."
            )

        self._recording = False

        stream = self._stream
        self._stream = None

        if stream is not None:
            try:
                stream.stop()
                stream.close()
            except Exception as error:
                logger.exception(
                    "Failed to close microphone stream"
                )

                raise VoiceError(
                    "Failed to stop microphone."
                ) from error

        with self._lock:
            audio = self._audio

        if audio is None or audio.size == 0:
            raise VoiceError(
                "No audio was recorded."
            )

        logger.info(
            "Voice recording stopped: %d samples",
            audio.size,
        )

        return audio

    def cancel_recording(self) -> None:
        """Cancel the current recording."""

        if not self._recording:
            return

        self._recording = False

        stream = self._stream
        self._stream = None

        if stream is not None:
            stream.stop()
            stream.close()

        with self._lock:
            self._audio = None

        logger.info("Voice recording cancelled")

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time: Any,
        status: sd.CallbackFlags,
    ) -> None:
        """Receive microphone samples."""

        if status:
            logger.warning(
                "Audio callback status: %s",
                status,
            )

        if not self._recording:
            return

        chunk = indata.copy()

        with self._lock:
            if self._audio is None:
                self._audio = chunk
            else:
                self._audio = np.concatenate(
                    (self._audio, chunk),
                    axis=0,
                )

    # ------------------------------------------------------------------
    # Compatibility API
    # ------------------------------------------------------------------

    def get_input(
        self,
        *,
        duration: float = 5.0,
    ) -> np.ndarray:
        """Record audio for a fixed duration.

        Kept for compatibility with existing code.
        """

        if duration <= 0:
            raise ValueError(
                "duration must be greater than 0"
            )

        self.start_recording()

        try:
            sd.sleep(
                int(duration * 1000)
            )

            return self.stop_recording()

        except Exception:
            self.cancel_recording()
            raise

    # ------------------------------------------------------------------
    # Speech recognition
    # ------------------------------------------------------------------

    def parse(
        self,
        input_data: Any,
    ) -> str:
        """Convert recorded audio into text."""

        if not isinstance(
            input_data,
            np.ndarray,
        ):
            raise VoiceError(
                "Invalid audio input."
            )

        if input_data.size == 0:
            raise VoiceError(
                "Audio input is empty."
            )

        logger.info(
            "Transcribing voice input"
        )

        try:
            segments, _ = self.model.transcribe(
                input_data,
                language="pt",
                beam_size=5,
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
                if segment.text.strip()
            ).strip()

        except Exception as error:
            logger.exception(
                "Failed to transcribe audio"
            )

            raise VoiceError(
                "Failed to transcribe voice input."
            ) from error

        if not text:
            raise VoiceError(
                "No speech detected."
            )

        logger.info(
            "Voice parsed successfully: %r",
            text,
        )

        return text

