import ffmpeg

def resize_with_ffmpeg(input_path, output_path, width, height, crf=18, preset='slow'):
    """
    Resize a video using FFmpeg while preserving high quality.
    """
    try:
        (
            ffmpeg
            .input(input_path)
            .filter('scale', width, height)
            .output(output_path, vcodec='libx264', crf=crf, preset=preset, acodec='aac')
            .run()
        )
        print(f"✅ Resized video saved to: {output_path}")
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        print("❌ FFmpeg Error:", error_message)

