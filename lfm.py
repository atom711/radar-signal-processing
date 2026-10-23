import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve


# 1. Setup Parameters & Time Vector
# 100 MHz ADC sample rate, 10 us pulse width, 20 MHz bandwidth
fs, T, B = 100e6, 10e-6, 20e6
# Fast-time vector centered at zero
t = np.arange(-T/2, T/2, 1/fs)
# Chirp rate (Hz/s)
K = B / T

# 2. Generate Reference Transmit Chirp & Matched Filter Template
# Complex LFM pulse
tx_chirp = np.exp(1j * np.pi * K * t**2)
# Matched filter: time-reversed & complex conjugated
h = np.conj(tx_chirp[::-1])

# 3. Simulate Received Signal (Target Return + Noise)
# Simulates target at a specific range delay
delay_samples = 400
# Padded received array
rx_signal = np.pad(tx_chirp, (delay_samples, 200))
noise = (np.random.randn(len(rx_signal)) + 1j * np.random.randn(len(rx_signal))) * 0.7
# Noisy target return
rx_noisy = rx_signal + noise

# 4. Perform Matched Filtering (Pulse Compression)
compressed_out = fftconvolve(rx_noisy, h, mode='same')
compressed_dB = 20 * np.log10(np.abs(compressed_out) / np.max(np.abs(compressed_out)))

# 5. Plot the Compressed Range Profile
plt.figure(figsize=(9, 4))
plt.plot(compressed_dB, label='Compressed Output (dB)', color='b')
plt.axhline(-13.2, color='r', linestyle='--', label='Ideal Unwindowed Sidelobe Level (-13.2 dB)')
plt.title('1D Range Pulse Compression (Matched Filter Output)')
plt.xlabel('Fast-Time Sample Index')
plt.ylabel('Normalized Magnitude (dB)')
plt.ylim(-40, 0); plt.grid(True); plt.legend()
plt.tight_layout()
output_name = "outputs/lfm_pulse_compression.png"
plt.savefig(output_name, dpi=300, bbox_inches="tight")
plt.show()