import io
import os
from datetime import datetime

import torchaudio
from loguru import logger
from openai import NotGiven
from pydantic import Field, field_validator
from silero_vad import collect_chunks, get_speech_timestamps, load_silero_vad, read_audio, save_audio

from plurally.models.env_vars import BaseEnvVars, OpenAiApiKeyRequired
from plurally.models.misc import AudioFile
from plurally.models.node import Node


class Transcript(Node):
    ICON = "openai"

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = OpenAiApiKeyRequired

    class InitSchema(Node.InitSchema):
        language: str = Field("", max_length=2, title="Language", description="The language of the audio file")
        vad_threshold: float = Field(
            0.3,
            title="VAD Threshold",
            lt=1.0,
            ge=0.0,
        )
        prompt: str = Field("")

        @field_validator("language", mode="before")
        def language_uppercase(cls, value):
            return value.strip().lower()

    class InputSchema(Node.InputSchema):
        audio: AudioFile = Field(
            title="Audio",
            description="The audio file",
            json_schema_extra={
                "type-friendly": "Audio",
            },
        )
        # FIXME: Prompt is buggy as hell and completely messes up the transcription
        # do not use it
        # prompt: str = Field(
        #     "",
        #     title="Prompt",
        #     description="The prompt to use for the transcription",
        #     json_schema_extra={
        #         "uiSchema": {"ui:widget": "textarea", "ui:options": {"rows": 10}}
        #     },
        # )

    class OutputSchema(Node.OutputSchema):
        transcript: str = Field(
            description="The extracted transcript from the audio file.",
        )

    def __init__(self, init_inputs: Node.InitSchema):
        self._client = None
        self.model = "whisper-1"
        self.language = init_inputs.language
        self.vad_threshold = init_inputs.vad_threshold
        self.prompt = init_inputs.prompt
        super().__init__(init_inputs)

    @property
    def client(self):
        global OpenAI
        from openai import OpenAI

        if self._client is None:
            self._client = OpenAI()
        return self._client

    def forward(self, node_inputs: InputSchema):
        logger.debug(f"Transcribing audio {node_inputs.audio.filename}")

        content = self.apply_vad(node_inputs.audio.content)

        if content is None:
            self.outputs = {"transcript": ""}
            return

        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=(node_inputs.audio.filename, content),
            language=self.language or NotGiven(),
            temperature=0,
            prompt=self.prompt or NotGiven(),
        )
        self.outputs = {"transcript": transcription.text}

    def serialize(self):
        return super().serialize() | {"language": self.language, "vad_threshold": self.vad_threshold, "prompt": self.prompt}

    def apply_vad(self, content):
        model = load_silero_vad()
        wav = read_audio(content)

        speech_timestamps = get_speech_timestamps(
            wav,
            model,
            threshold=self.vad_threshold,
        )
        if not speech_timestamps:
            return None
        voiced_audio = collect_chunks(speech_timestamps, wav)
        bio = io.BytesIO()
        torchaudio.save(bio, voiced_audio.unsqueeze(0), 16000, bits_per_sample=16, format="wav")
        bio.seek(0)
        return bio
