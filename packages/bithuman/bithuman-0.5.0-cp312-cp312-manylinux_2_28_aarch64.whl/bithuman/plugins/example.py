import argparse
import asyncio
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from bithuman.plugins.stt import BithumanLocalSTT


async def transcribe_file(file_path, locale="en-US", on_device=False, debug=False):
    print(f"Reading audio file: {file_path}")

    # Read and process audio file
    audio_data, sample_rate = sf.read(file_path, dtype="float32")
    print(f"Sample rate: {sample_rate} Hz")

    # Convert to mono if stereo
    if len(audio_data.shape) > 1:
        print("Converting stereo to mono")
        audio_data = audio_data.mean(axis=1)

    # Initialize STT (will use bundled binary by default)
    print(f"Initializing speech recognition with locale: {locale}")
    try:
        async with BithumanLocalSTT(
            locale=locale,
            on_device=on_device,
            punctuation=True,
            debug=debug,  # Enable or disable debug output
        ) as stt:
            # Convert to int16 for recognition
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Create a single audio frame from the data
            from livekit import rtc
            frame = rtc.AudioFrame(
                data=audio_int16.tobytes(),
                sample_rate=sample_rate,
                num_channels=1,
                samples_per_channel=len(audio_int16)
            )

            # Recognize speech
            print("Recognizing speech...")
            start_time = time.time()
            event = await stt.recognize(frame)
            end_time = time.time()

            # Extract the results from the event
            result = {
                "text": event.alternatives[0].text if event.alternatives else "",
                "confidence": event.alternatives[0].confidence if event.alternatives else 0.0
            }

            # Print results
            print("\nResults:")
            print(f"Transcription: {result['text']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Process time: {(end_time - start_time):.2f} seconds")

            return result
    except RuntimeError as e:
        print(f"Error: {str(e)}")
        return None


async def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using Bithuman Local Voice"
    )
    parser.add_argument("audio_file", help="Path to audio file to transcribe")
    parser.add_argument(
        "--locale",
        default="en-US",
        help="Locale for transcription (e.g., en-US, fr-FR)",
    )
    parser.add_argument(
        "--on-device", action="store_true", help="Use on-device recognition only"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with detailed error messages",
    )

    args = parser.parse_args()

    if not Path(args.audio_file).exists():
        print(f"Error: Audio file not found: {args.audio_file}")
        return

    await transcribe_file(args.audio_file, args.locale, args.on_device, args.debug)


if __name__ == "__main__":
    asyncio.run(main())
