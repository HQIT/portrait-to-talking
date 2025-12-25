"""
Command-line interface for portrait-to-talking.
"""

import argparse
import sys
import logging

from .client import TalkingVideoClient, GenerationError
from .providers.base import GenerationResult


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog="portrait-to-talking",
        description="Generate talking video from portrait image"
    )
    
    # Required arguments
    parser.add_argument(
        "image",
        help="Portrait image path or URL"
    )
    
    # Audio options
    parser.add_argument(
        "-a", "--audio",
        help="Audio file path or URL (optional, generates silent video if not provided)"
    )
    
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Generate silent video (no audio)"
    )
    
    # Output options
    parser.add_argument(
        "-o", "--output",
        help="Output video file path"
    )
    
    # Generation options
    parser.add_argument(
        "--face-crop-ratio",
        type=float,
        default=2.0,
        help="Face crop dilation ratio (default: 2.0)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        default=256,
        help="Output video height (default: 256)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        help="Output video width (optional)"
    )
    
    # Provider options
    parser.add_argument(
        "--echomimic-url",
        help="EchoMimic service URL (default: from ECHOMIMIC_URL env var)"
    )
    
    # Logging
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Determine audio
    audio = None if args.silent else args.audio
    
    try:
        # Create progress callback
        def on_complete(result: GenerationResult):
            if result.success:
                logger.info(f"Generation completed: {result.output_path}")
            else:
                logger.error(f"Generation failed: {result.error}")
        
        # Create client and generate
        client = TalkingVideoClient(
            image=args.image,
            audio=audio,
            face_crop_ratio=args.face_crop_ratio,
            height=args.height,
            width=args.width,
            echomimic_url=args.echomimic_url,
            callback=on_complete if args.verbose else None
        )
        
        logger.info(f"Generating talking video from: {args.image}")
        if audio:
            logger.info(f"Using audio: {audio}")
        else:
            logger.info("Generating silent video")
        
        result = client.generate(output_path=args.output)
        
        print(f"Video generated successfully")
        print(f"Output path: {result.output_path}")
        
    except GenerationError as e:
        logger.error(f"Generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

