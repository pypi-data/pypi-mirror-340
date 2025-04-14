import vidtoolz
import os


from moviepy import (
    VideoFileClip,
    AudioFileClip,
    concatenate_audioclips,
    CompositeAudioClip,
    afx,
)


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_audio.mp4")


def add_audio_to_video(
    video_file, audio_file, output_file, original_audio_volume=50, startat=0
):
    """
    Adds an external audio track to a video file, lowering the original audio by a specified percentage.
    If the external audio is shorter than the video, it is looped to match the video's duration.

    Parameters:
        video_file (str): Path to the video file.
        audio_file (str): Path to the audio file.
        output_file (str): Path to save the output video.
        original_audio_volume (float): Percentage to lower the original audio (0-100).
    """
    # Load the video file
    video = VideoFileClip(video_file)

    # Load the audio file
    audio = AudioFileClip(audio_file)
    audio = audio.subclipped(start_time=startat)

    # Adjust original audio volume
    # original_audio = video.audio.volumex()
    original_audio = video.audio.with_effects(
        [afx.MultiplyVolume(original_audio_volume / 100.0)]
    )

    # Repeat the audio to match video duration
    audio_duration = audio.duration
    video_duration = video.duration
    if audio_duration < video_duration:
        num_repeats = int(video_duration // audio_duration) + 1
        audio = concatenate_audioclips([audio] * num_repeats)

    # Trim the audio to match video duration
    audio = audio.subclipped(0, video_duration)

    # Combine the original and new audio tracks
    # combined_audio = original_audio.audio_fadeout(1).fx("audio_mix", audio)
    combined_audio = CompositeAudioClip([original_audio, audio])

    # Set the new audio to the video
    video_with_new_audio = video.with_audio(combined_audio)

    # Write the output video
    video_with_new_audio.write_videofile(
        output_file, codec="libx264", audio_codec="aac"
    )
    return output_file


def create_parser(subparser):
    parser = subparser.add_parser(
        "repaudio", description="Replace audio for a video file"
    )
    parser.add_argument("video", type=str, help="Path to the input video file")
    parser.add_argument("audio", type=str, help="Path to the audio file")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to save the output video. Default None",
    )
    parser.add_argument(
        "-v",
        "--volume",
        type=float,
        default=30,
        help="Percentage to lower the original audio (0-100), Default 30",
    )

    parser.add_argument(
        "-s",
        "--startat",
        type=float,
        default=0.0,
        help="Load audio at this time in seconds. Default 0",
    )
    return parser


class ViztoolzPlugin:
    """Replace audio for a video file"""

    __name__ = "repaudio"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        output = determine_output_path(args.video, args.output)
        _ = add_audio_to_video(
            args.video, args.audio, output, args.volume, args.startat
        )

    def hello(self, args):
        # this routine will be called when "vidtoolz "repaudio is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


repaudio_plugin = ViztoolzPlugin()
