# Improved Icelandic TTS Guide

We've successfully created and tuned a Text-to-Speech solution for Icelandic that produces decent results with minimal resource requirements.

## Our Approach

We've optimized the standard TTS engines to better handle Icelandic pronunciation by:

1. Using espeak/pyttsx3 as a lightweight TTS engine
1. Slowing down the speech rate (80-100 WPM) to improve pronunciation
1. Testing different voices for the best Icelandic compatibility
1. Creating a tuning system to find optimal parameters

## Results

We generated several different variations of the TTS with different parameters:

| Version | Speech Rate | Voice | Quality Observations |
|---------|------------|-------|----------------------|
| rate_80 | 80 WPM | Default | Slower, clearer Icelandic pronunciation |
| rate_100 | 100 WPM | Default | Decent balance of speed and clarity |
| rate_150 | 150 WPM | Default | Faster but less accurate pronunciation |
| voice_1 | 120 WPM | Female | Different voice quality, better for certain sounds |
| voice_2 | 120 WPM | Male | Alternative voice option |

All audio samples are available in the `improved_tts_samples/tuning/` directory.

## How to Use

```bash
# Basic usage
python improved_icelandic_tts.py --text "Your Icelandic text here"

# Use slower rate for better pronunciation
python improved_icelandic_tts.py --rate 80

# Try different voices
python improved_icelandic_tts.py --voice 1

# Test multiple parameter combinations
python improved_icelandic_tts.py --tune
```

## Advanced Voice Options

For even better Icelandic pronunciation, these are the recommended approaches:

1. **Bark TTS** (requires more resources):

```bash
pip install git+https://github.com/suno-ai/bark.git
python test_bark_tts.py
```

1. **XTTS with Voice Cloning** (requires more resources):

```bash
pip install TTS
python test_xtts.py
```

1. **Commercial Options**:
   - Tiro.is - Specialized Icelandic TTS service
   - Azure Custom Neural Voice - Train on native Icelandic speech

## Tips for Better Icelandic Pronunciation

1. **Slow down the speech rate** - Icelandic has complex sounds that need more time to articulate

1. **Use SSML to help with difficult sounds**:

```xml
<speak>
  <prosody rate="slow">
    Góðan daginn. Þetta er <emphasis>prófun</emphasis> á íslensku.
  </prosody>
</speak>
```

1. **Post-process audio** if needed:
   - Increase bass slightly to improve authentic sound
   - Normalize audio levels for clarity
   - Apply subtle reverb to make synthetic voice more natural

## Files Generated

- `improved_icelandic_tts.py` - Main script for generating improved TTS
- `improved_tts_samples/` - Directory containing generated audio files
- `test_bark_tts.py` - Advanced TTS with Bark (if resources permit)
- `test_xtts.py` - Advanced TTS with voice cloning (if resources permit)

## Next Steps

The current solution provides a good balance of quality and resource usage. For further improvements:

1. Record a native Icelandic speaker for reference/training
1. Test with more specialized Icelandic text samples
1. Consider Icelandic language-specific commercial services