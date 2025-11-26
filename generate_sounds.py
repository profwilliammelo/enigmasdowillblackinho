import wave
import math
import struct
import random

def save_wav(filename, data, sample_rate=44100):
    with wave.open(filename, 'w') as f:
        f.setnchannels(2)  # Stereo
        f.setsampwidth(2)  # 2 bytes per sample (16-bit PCM)
        f.setframerate(sample_rate)
        
        # Convert float samples (-1.0 to 1.0) to 16-bit integers
        packed_data = b''
        for sample in data:
            # Clip to range
            sample = max(-1.0, min(1.0, sample))
            val = int(sample * 32767)
            # Write twice for stereo (Left + Right)
            packed_data += struct.pack('<h', val)
            packed_data += struct.pack('<h', val)
            
        f.writeframes(packed_data)
    print(f"Generated {filename}")

def generate_sine_wave(freq, duration, sample_rate=44100):
    n_frames = int(duration * sample_rate)
    data = []
    for i in range(n_frames):
        t = i / sample_rate
        val = math.sin(2 * math.pi * freq * t)
        # Apply simple envelope (fade out)
        envelope = 1.0 - (i / n_frames)
        data.append(val * envelope)
    return data

def generate_square_wave(freq, duration, sample_rate=44100):
    n_frames = int(duration * sample_rate)
    data = []
    for i in range(n_frames):
        t = i / sample_rate
        # Square wave logic
        val = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
        # Envelope
        envelope = 1.0 - (i / n_frames)
        data.append(val * envelope)
    return data

def generate_jump_sound():
    # Slide whistle up (Square wave for retro feel)
    sample_rate = 44100
    duration = 0.2
    n_frames = int(duration * sample_rate)
    data = []
    for i in range(n_frames):
        t = i / sample_rate
        freq = 300 + (600 * (i / n_frames)) # 300 -> 900 Hz
        val = 0.6 if math.sin(2 * math.pi * freq * t) > 0 else -0.6
        data.append(val)
    save_wav('pulo.wav', data)

def generate_coin_sound():
    # High ping (Sine wave is fine, but higher volume)
    data = []
    data.extend(generate_sine_wave(1200, 0.08))
    data.extend(generate_sine_wave(1800, 0.15))
    # Boost volume
    data = [min(1.0, d * 1.5) for d in data]
    save_wav('moeda.wav', data)

def generate_correct_sound():
    # Power up arpeggio
    data = []
    # C Major chord fast
    data.extend(generate_square_wave(523.25, 0.08)) # C5
    data.extend(generate_square_wave(659.25, 0.08)) # E5
    data.extend(generate_square_wave(783.99, 0.08)) # G5
    data.extend(generate_square_wave(1046.50, 0.2)) # C6
    save_wav('acerto.wav', data)

def generate_levelup_sound():
    # Victory fanfare
    data = []
    notes = [(523.25, 0.1), (523.25, 0.1), (523.25, 0.1), (659.25, 0.3), (783.99, 0.3), (1046.50, 0.6)]
    for freq, dur in notes:
        data.extend(generate_square_wave(freq, dur))
    save_wav('levelup.wav', data)

def generate_error_sound():
    # Low buzz
    data = generate_square_wave(100, 0.4)
    save_wav('erro.wav', data)

def generate_music():
    # Simple 4/4 beat loop
    sample_rate = 44100
    bpm = 120
    beat_dur = 60 / bpm
    
    # Kick drum (low sine sweep)
    def kick():
        dur = 0.2
        frames = int(dur * sample_rate)
        d = []
        for i in range(frames):
            t = i/sample_rate
            freq = 150 - (140 * (i/frames))
            d.append(math.sin(2*math.pi*freq*t) * 0.8 * (1-i/frames))
        return d + [0.0] * int((beat_dur - dur) * sample_rate)

    # Snare (noise)
    def snare():
        dur = 0.15
        frames = int(dur * sample_rate)
        d = []
        for i in range(frames):
            d.append(random.uniform(-0.5, 0.5) * (1-i/frames))
        return d + [0.0] * int((beat_dur - dur) * sample_rate)
    
    # Hi-hat (short noise)
    def hat():
        dur = 0.05
        frames = int(dur * sample_rate)
        d = []
        for i in range(frames):
            d.append(random.uniform(-0.3, 0.3) * (1-i/frames))
        return d + [0.0] * int((beat_dur/2 - dur) * sample_rate)

    track = []
    # Pattern: Kick - Hat - Snare - Hat (x4 for a loop)
    for _ in range(4):
        # Beat 1: Kick
        track.extend(kick())
        # Beat 2: Snare
        track.extend(snare())
        # Beat 3: Kick
        track.extend(kick())
        # Beat 4: Snare
        track.extend(snare())
        
    save_wav('music.wav', track)

if __name__ == "__main__":
    generate_jump_sound()
    generate_coin_sound()
    generate_correct_sound()
    generate_levelup_sound()
    generate_error_sound()
    generate_music()
