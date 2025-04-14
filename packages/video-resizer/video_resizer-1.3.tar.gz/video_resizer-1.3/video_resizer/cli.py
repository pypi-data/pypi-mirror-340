import argparse
from video_resizer.resizer import resize_with_ffmpeg

def main():
    parser = argparse.ArgumentParser(description='Resize video using FFmpeg.')
    parser.add_argument('input', help='Input video file')
    parser.add_argument('output', help='Output video file')
    parser.add_argument('--width', type=int, required=True)
    parser.add_argument('--height', type=int, required=True)
    parser.add_argument('--crf', type=int, default=18)
    parser.add_argument('--preset', type=str, default='slow')
    
    args = parser.parse_args()
    
    resize_with_ffmpeg(args.input, args.output, args.width, args.height, args.crf, args.preset)
