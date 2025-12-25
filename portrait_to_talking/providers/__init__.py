"""
Talking Video Providers - 不同数字人视频生成服务的适配器
"""

from .base import TalkingVideoProvider
from .echomimic import EchoMimicProvider

__all__ = ["TalkingVideoProvider", "EchoMimicProvider"]

