from __future__ import annotations

import webbrowser

def set_brightness(level: int) -> str:
    """Laptop brightness level set karta hai (0-100)."""
    if not 0 <= level <= 100:
        raise ValueError("Brightness must be between 0 and 100")
    import screen_brightness_control as sbc

    sbc.set_brightness(level)
    return f"Brightness set to {level}%"

def set_volume(level: int) -> str:
    """System volume set karta hai (0-100)."""
    if not 0 <= level <= 100:
        raise ValueError("Volume must be between 0 and 100")
    from ctypes import POINTER, cast

    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Scale 0-100 to Scalar 0.0 - 1.0
    scalar_level = max(0.0, min(1.0, level / 100.0))
    volume.SetMasterVolumeLevelScalar(scalar_level, None)
    return f"Volume set to {level}%"

def play_youtube_video(query: str) -> str:
    """YouTube par search karke video open karta hai."""
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Playing '{query}' on YouTube"