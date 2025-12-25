"""
portrait-to-talking: Generate talking video from portrait image.
"""

from .client import TalkingVideoClient, GenerationError, generate_talking_video
from .providers import TalkingVideoProvider, EchoMimicProvider
from .providers.base import GenerationConfig, GenerationResult

__version__ = "0.1.0"
__all__ = [
    "TalkingVideoClient",
    "GenerationError",
    "generate_talking_video",
    "TalkingVideoProvider",
    "EchoMimicProvider",
    "GenerationConfig",
    "GenerationResult",
]

