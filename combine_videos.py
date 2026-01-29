#!/usr/bin/env python3
"""Combine speaker videos side-by-side for 2spk and 3spk separation samples."""

import os
import subprocess
from pathlib import Path

def combine_videos_2spk():
    """Combine 2-speaker videos side-by-side."""
    base_path = Path("samples/2_spk_separation")
    scenarios = [
        "separation_vox2_dcase",
        "separation_vox2_dns_0db",
        "separation_vox2_dns_5db"
    ]
    
    for scenario in scenarios:
        scenario_path = base_path / scenario / "speakers"
        spk1_video = scenario_path / "spk1" / "reference.mp4"
        spk2_video = scenario_path / "spk2" / "reference.mp4"
        output_video = scenario_path / "mixture.mp4"
        
        if spk1_video.exists() and spk2_video.exists():
            print(f"Combining: {scenario}")
            # Remove existing file
            if output_video.exists():
                os.remove(output_video)
            cmd = [
                "ffmpeg", "-i", str(spk1_video), "-i", str(spk2_video),
                "-filter_complex", "[0:v][1:v]hstack=inputs=2[v]",
                "-map", "[v]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k",
                str(output_video)
            ]
            subprocess.run(cmd, check=True)
            print(f"Created: {output_video}")

def combine_videos_3spk():
    """Combine 3-speaker videos in a grid (1 top, 2 bottom)."""
    base_path = Path("samples/3_spk_separation")
    scenarios = [
        "separation_vox2_dcase",
        "separation_vox2_dns"
    ]
    
    for scenario in scenarios:
        scenario_path = base_path / scenario / "speakers"
        spk1_video = scenario_path / "spk1" / "reference.mp4"
        spk2_video = scenario_path / "spk2" / "reference.mp4"
        spk3_video = scenario_path / "spk3" / "reference.mp4"
        output_video = scenario_path / "mixture.mp4"
        
        if spk1_video.exists() and spk2_video.exists() and spk3_video.exists():
            print(f"Combining: {scenario}")
            # Remove existing file
            if output_video.exists():
                os.remove(output_video)
            # Create a 3-video grid: spk1 on top (2x width), spk2 and spk3 below (1x width each)
            cmd = [
                "ffmpeg",
                "-i", str(spk1_video), "-i", str(spk2_video), "-i", str(spk3_video),
                "-filter_complex",
                "[0:v]scale=480:270[top];"
                "[1:v]scale=240:270[left];"
                "[2:v]scale=240:270[right];"
                "[top][left][right]xstack=inputs=3:layout=0_0|0_h0|w0_h0[v]",
                "-map", "[v]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k",
                str(output_video)
            ]
            subprocess.run(cmd, check=True)
            print(f"Created: {output_video}")

def combine_enhancement_videos():
    """Enhancement only has 1 speaker, so no combining needed."""
    print("Enhancement videos are single-speaker, no combining needed.")

if __name__ == "__main__":
    print("Combining speaker videos...")
    combine_videos_2spk()
    combine_videos_3spk()
    combine_enhancement_videos()
    print("Done!")
