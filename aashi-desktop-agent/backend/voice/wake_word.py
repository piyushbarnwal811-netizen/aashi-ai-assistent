from __future__ import annotations

import struct
from backend.config import config

def listen_for_wake_word(callback):
    """
    Background me 'AASHI' hotword ko continuously sunta hai bina CPU load ke.
    """
    porcupine = None
    audio_stream = None
    pa = None

    try:
        import pyaudio
        import pvporcupine

        # Agar picovoice key ho to porcupine use karega, nahi to simple fallback
        if config.picovoice_key:
            porcupine = pvporcupine.create(
            access_key=config.picovoice_key,
                keywords=["porcupine"]  # Custom 'AASHI' keyword ppn file path can be passed here
            )
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

            print("🎙️ AASHI Wake-Word Engine Active...")
            while True:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("⚡ Wake Word Detected: AASHI!")
                    callback()
        else:
            print("⚠️ Picovoice Key not found. Manual trigger enabled.")

    except Exception as e:
        print(f"Error in Wake Word Listener: {e}")
    finally:
        if audio_stream:
            audio_stream.close()
        if pa:
            pa.terminate()
        if porcupine:
            porcupine.delete()