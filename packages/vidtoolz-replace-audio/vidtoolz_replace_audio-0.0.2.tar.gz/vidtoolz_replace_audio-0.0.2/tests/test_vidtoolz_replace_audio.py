import pytest
import vidtoolz_replace_audio as w
import os

from moviepy import ColorClip, AudioFileClip, afx, CompositeAudioClip
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np

from argparse import ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["video.mp4", "audio.mp3"])
    assert result.video == "video.mp4"
    assert result.audio == "audio.mp3"
    assert result.output is None
    assert result.volume == 30
    assert result.startat == 0.0


def test_plugin(capsys):
    w.repaudio_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@pytest.fixture
def sample_video(tmp_path):
    # Create a 2-second color video with silent audio
    video = ColorClip(size=(320, 240), color=(255, 0, 0), duration=4)
    silent_audio = AudioArrayClip(np.zeros((44100 * 2, 1)), fps=44100)
    video = video.with_audio(silent_audio)
    video_file = tmp_path / "sample_video.mp4"
    video.write_videofile(
        str(video_file), fps=24, codec="libx264", audio_codec="aac", logger=None
    )
    return str(video_file)


@pytest.fixture
def sample_audio(tmp_path):
    # Create a 1-second sine wave tone
    duration = 1  # seconds
    freq = 440  # Hz
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * freq * t)
    audio_clip = AudioArrayClip(sine_wave.reshape(-1, 1), fps=sample_rate)
    audio_file = tmp_path / "sample_audio.wav"
    audio_clip.write_audiofile(str(audio_file), fps=sample_rate, logger=None)
    return str(audio_file)


def test_add_audio_to_video_creates_output(tmp_path, sample_video, sample_audio):
    output_file = tmp_path / "output_video.mp4"

    result_file = w.add_audio_to_video(
        video_file=sample_video,
        audio_file=sample_audio,
        output_file=str(output_file),
        original_audio_volume=50,
    )

    assert os.path.exists(result_file)
    assert os.path.getsize(result_file) > 0

    # Optional: Load result video and check duration/audio
    from moviepy import VideoFileClip

    clip = VideoFileClip(result_file)
    assert clip.audio is not None
    assert clip.duration == 4  # Allow small timing error
