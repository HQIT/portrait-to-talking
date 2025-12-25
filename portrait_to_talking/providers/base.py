"""
Talking Video Provider 基类
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class GenerationConfig:
    """视频生成配置"""
    face_crop_ratio: float = 2.0
    height: int = 256
    width: Optional[int] = None
    extra: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


@dataclass 
class GenerationResult:
    """生成结果"""
    success: bool
    output_path: Optional[str] = None
    video_data: Optional[bytes] = None
    error: Optional[str] = None


class TalkingVideoProvider(ABC):
    """
    数字人视频生成服务提供者基类。
    
    所有数字人视频生成服务适配器都应继承此类并实现 generate 方法。
    """
    
    @abstractmethod
    def generate(
        self,
        image: str,
        audio: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> GenerationResult:
        """
        根据肖像图片和音频生成讲话视频。
        
        Args:
            image: 肖像图片路径或 URL
            audio: 音频文件路径或 URL（可选，无则生成静默视频）
            config: 生成配置
            
        Returns:
            GenerationResult 生成结果
        """
        pass
    
    @property
    def name(self) -> str:
        """Provider 名称"""
        return self.__class__.__name__

