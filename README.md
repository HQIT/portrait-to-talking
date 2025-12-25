# portrait-to-talking

根据肖像照片生成数字人讲话视频。

## 功能特性

- 支持根据肖像照片生成讲话视频
- 支持生成静默视频（无音频）
- 支持多种数字人生成服务（EchoMimic 等）
- 命令行工具和 Python API 两种使用方式
- **Provider 抽象层**，可扩展支持不同服务

## 安装

### 从源码安装

```bash
cd portrait-to-talking
pip install -e .
```

## 配置

设置环境变量（可选）：

```bash
export ECHOMIMIC_URL="http://localhost:8000/a2v"
export ECHOMIMIC_WAV_SILENT="http://server/silent.wav"
export ECHOMIMIC_WAV_TALKING="http://server/talking.wav"
```

或创建 `.env` 文件：

```
ECHOMIMIC_URL=http://localhost:8000/a2v
ECHOMIMIC_WAV_SILENT=http://server/silent.wav
ECHOMIMIC_WAV_TALKING=http://server/talking.wav
```

## 命令行使用

### 基本用法

```bash
# 生成讲话视频
portrait-to-talking portrait.jpg -a speech.wav -o output.mp4

# 生成静默视频
portrait-to-talking portrait.jpg --silent -o silent.mp4

# 使用 URL
portrait-to-talking http://server/portrait.jpg -a http://server/audio.wav
```

### 选项

```bash
# 指定人脸裁剪比例
portrait-to-talking portrait.jpg -a audio.wav --face-crop-ratio 2.5

# 指定输出视频高度
portrait-to-talking portrait.jpg -a audio.wav --height 512

# 指定 EchoMimic 服务 URL
portrait-to-talking portrait.jpg -a audio.wav --echomimic-url http://localhost:8000/a2v

# 详细输出
portrait-to-talking portrait.jpg -a audio.wav -v
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `image` | 肖像图片路径或 URL（必需） |
| `-a, --audio` | 音频文件路径或 URL |
| `--silent` | 生成静默视频 |
| `-o, --output` | 输出视频文件路径 |
| `--face-crop-ratio` | 人脸裁剪比例（默认 2.0） |
| `--height` | 输出视频高度（默认 256） |
| `--width` | 输出视频宽度 |
| `--echomimic-url` | EchoMimic 服务 URL |
| `-v, --verbose` | 详细输出 |
| `--version` | 显示版本号 |

## Python API

### 基本用法

```python
from portrait_to_talking import TalkingVideoClient

# 生成讲话视频
client = TalkingVideoClient(
    image="portrait.jpg",
    audio="speech.wav"
)
result = client.generate()
print(result.output_path)

# 生成静默视频
client = TalkingVideoClient(image="portrait.jpg")
result = client.generate()
```

### 使用自定义 Provider

```python
from portrait_to_talking import TalkingVideoClient, EchoMimicProvider

# 创建自定义 provider
provider = EchoMimicProvider(url="http://custom-server:8000/a2v")

# 使用 provider 创建客户端
client = TalkingVideoClient(
    image="portrait.jpg",
    audio="speech.wav",
    provider=provider
)
result = client.generate()
```

### 便捷函数

```python
from portrait_to_talking import generate_talking_video

# 一行代码生成视频
result = generate_talking_video(
    image="portrait.jpg",
    audio="speech.wav"
)
```

### 配置参数

```python
from portrait_to_talking import TalkingVideoClient

client = TalkingVideoClient(
    image="portrait.jpg",
    audio="speech.wav",
    face_crop_ratio=2.5,  # 人脸裁剪比例
    height=512,           # 输出高度
    width=512             # 输出宽度
)
```

## 扩展服务

通过实现 `TalkingVideoProvider` 基类，可以添加新的数字人生成服务：

```python
from portrait_to_talking.providers import TalkingVideoProvider
from portrait_to_talking.providers.base import GenerationConfig, GenerationResult

class SadTalkerProvider(TalkingVideoProvider):
    def __init__(self, url: str):
        self.url = url
    
    def generate(self, image, audio, config) -> GenerationResult:
        # 实现 SadTalker 调用逻辑
        ...
        return GenerationResult(success=True, output_path="...")

# 使用自定义 provider
provider = SadTalkerProvider(url="http://sadtalker-server/api")
client = TalkingVideoClient(image="portrait.jpg", provider=provider)
```

## API 参考

### TalkingVideoClient

```python
TalkingVideoClient(
    image: str,                    # 肖像图片路径或 URL
    audio: str = None,             # 音频文件路径或 URL
    provider: TalkingVideoProvider = None,  # 服务提供者
    face_crop_ratio: float = 2.0,  # 人脸裁剪比例
    height: int = 256,             # 输出视频高度
    width: int = None,             # 输出视频宽度
    callback: Callable = None      # 完成回调
)
```

### GenerationResult

```python
@dataclass
class GenerationResult:
    success: bool           # 是否成功
    output_path: str        # 输出视频路径
    video_data: bytes       # 视频数据（可选）
    error: str              # 错误信息
```

### TalkingVideoProvider

```python
class TalkingVideoProvider(ABC):
    @abstractmethod
    def generate(self, image, audio, config) -> GenerationResult:
        """生成数字人视频"""
        pass
```

## 作为模块运行

```bash
python -m portrait_to_talking portrait.jpg -a audio.wav
```

## License

MIT License

