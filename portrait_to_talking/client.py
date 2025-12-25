"""
Core client for portrait-to-talking video generation.
"""

import logging
from typing import Optional, Callable

from .providers import TalkingVideoProvider, EchoMimicProvider
from .providers.base import GenerationConfig, GenerationResult

logger = logging.getLogger(__name__)


class GenerationError(Exception):
    """Exception raised when video generation fails."""
    pass


class TalkingVideoClient:
    """
    数字人讲话视频生成客户端。
    
    Example:
        >>> client = TalkingVideoClient(image="portrait.jpg", audio="speech.wav")
        >>> result = client.generate()
        >>> print(result.output_path)
        
        # 使用自定义 provider
        >>> from portrait_to_talking.providers import EchoMimicProvider
        >>> provider = EchoMimicProvider(url="http://custom-server/a2v")
        >>> client = TalkingVideoClient(image="portrait.jpg", provider=provider)
    """
    
    def __init__(
        self,
        image: str,
        audio: Optional[str] = None,
        provider: Optional[TalkingVideoProvider] = None,
        face_crop_ratio: float = 2.0,
        height: int = 256,
        width: Optional[int] = None,
        callback: Optional[Callable[[GenerationResult], None]] = None,
        # 向后兼容
        echomimic_url: Optional[str] = None
    ):
        """
        初始化客户端。
        
        Args:
            image: 肖像图片路径或 URL
            audio: 音频文件路径或 URL（可选，无则生成静默视频）
            provider: 视频生成服务提供者
            face_crop_ratio: 人脸裁剪扩展比例
            height: 输出视频高度
            width: 输出视频宽度（可选）
            callback: 完成回调函数
            echomimic_url: EchoMimic 服务 URL（向后兼容）
        """
        self.image = image
        self.audio = audio
        self.callback = callback
        
        self.config = GenerationConfig(
            face_crop_ratio=face_crop_ratio,
            height=height,
            width=width
        )
        
        # Provider 优先，否则使用默认 EchoMimicProvider
        if provider:
            self.provider = provider
        else:
            self.provider = EchoMimicProvider(url=echomimic_url)
    
    def generate(self, output_path: Optional[str] = None) -> GenerationResult:
        """
        生成数字人讲话视频。
        
        Args:
            output_path: 输出文件路径（可选，用于下载远程生成的视频）
            
        Returns:
            GenerationResult
            
        Raises:
            GenerationError: 如果生成失败
        """
        logger.info(f"Generating talking video from: {self.image}")
        
        result = self.provider.generate(
            image=self.image,
            audio=self.audio,
            config=self.config
        )
        
        if self.callback:
            self.callback(result)
        
        if not result.success:
            raise GenerationError(result.error)
        
        # 如果指定了输出路径且有远程路径，可以下载
        if output_path and result.output_path:
            logger.info(f"Video generated at: {result.output_path}")
            # 注意：实际下载逻辑需要根据部署环境实现
            # 这里只记录路径
        
        return result


def generate_talking_video(
    image: str,
    audio: Optional[str] = None,
    output_path: Optional[str] = None,
    provider: Optional[TalkingVideoProvider] = None,
    face_crop_ratio: float = 2.0,
    height: int = 256,
    **kwargs
) -> GenerationResult:
    """
    便捷函数：生成数字人讲话视频。
    
    Args:
        image: 肖像图片路径或 URL
        audio: 音频文件路径或 URL
        output_path: 输出文件路径
        provider: 视频生成服务提供者
        face_crop_ratio: 人脸裁剪比例
        height: 输出视频高度
        
    Returns:
        GenerationResult
    """
    client = TalkingVideoClient(
        image=image,
        audio=audio,
        provider=provider,
        face_crop_ratio=face_crop_ratio,
        height=height,
        **kwargs
    )
    return client.generate(output_path=output_path)

