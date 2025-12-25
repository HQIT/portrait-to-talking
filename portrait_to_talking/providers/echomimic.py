"""
EchoMimic Provider - EchoMimic 数字人视频生成服务适配器
"""

import os
import logging
from typing import Optional

import requests
from dotenv import load_dotenv

from .base import TalkingVideoProvider, GenerationConfig, GenerationResult

load_dotenv()
logger = logging.getLogger(__name__)

DEFAULT_URL = os.getenv("ECHOMIMIC_URL", "http://localhost:8000/a2v")
DEFAULT_SILENT_AUDIO = os.getenv("ECHOMIMIC_WAV_SILENT", "")
DEFAULT_TALKING_AUDIO = os.getenv("ECHOMIMIC_WAV_TALKING", "")


class EchoMimicProvider(TalkingVideoProvider):
    """
    EchoMimic 数字人视频生成服务提供者。
    
    通过调用 EchoMimic HTTP API 生成数字人讲话视频。
    
    Example:
        >>> provider = EchoMimicProvider(url="http://localhost:8000/a2v")
        >>> result = provider.generate("portrait.jpg", "speech.wav")
        >>> print(result.output_path)
    """
    
    def __init__(
        self,
        url: str = None,
        silent_audio: str = None,
        talking_audio: str = None,
        timeout: int = 300
    ):
        """
        初始化 EchoMimic Provider。
        
        Args:
            url: EchoMimic 服务 URL
            silent_audio: 静默音频 URL（用于生成静默视频）
            talking_audio: 讲话音频 URL（用于生成讲话样本视频）
            timeout: 请求超时时间（秒）
        """
        self.url = url or DEFAULT_URL
        self.silent_audio = silent_audio or DEFAULT_SILENT_AUDIO
        self.talking_audio = talking_audio or DEFAULT_TALKING_AUDIO
        self.timeout = timeout
    
    def generate(
        self,
        image: str,
        audio: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> GenerationResult:
        """
        调用 EchoMimic 生成数字人视频。
        
        Args:
            image: 肖像图片路径或 URL
            audio: 音频文件路径或 URL（可选）
            config: 生成配置
            
        Returns:
            GenerationResult
        """
        config = config or GenerationConfig()
        
        # 如果没有音频，使用静默音频
        if not audio:
            audio = self.silent_audio
        
        # 构建请求数据
        data = {
            "ref_image_url": image,
            "audio_url": audio,
            "config": {
                "facecrop_dilation_ratio": config.face_crop_ratio,
                "height": config.height,
            }
        }
        
        if config.width:
            data["config"]["width"] = config.width
        
        if config.extra:
            data["config"].update(config.extra)
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"Calling EchoMimic: {self.url}")
            logger.debug(f"Request data: {data}")
            
            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            output_path = result.get("output_path", "")
            
            # 确保路径格式正确
            if output_path and not output_path.startswith("/"):
                output_path = "/" + output_path
            
            logger.info(f"EchoMimic generation successful: {output_path}")
            
            return GenerationResult(
                success=True,
                output_path=output_path
            )
            
        except requests.exceptions.Timeout:
            error_msg = "EchoMimic request timeout"
            logger.error(error_msg)
            return GenerationResult(success=False, error=error_msg)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"EchoMimic request failed: {e}"
            logger.error(error_msg)
            return GenerationResult(success=False, error=error_msg)
            
        except Exception as e:
            error_msg = f"EchoMimic generation failed: {e}"
            logger.error(error_msg)
            return GenerationResult(success=False, error=error_msg)
    
    @property
    def name(self) -> str:
        return "echomimic"

