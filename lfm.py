import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
# 1. Setup Parameters & Time Vector
fs, T, B = 100e6, 10e-6, 20e6                     # 100 MHz sample rate, 10 us pulse width, 20 MHz bandwidth
t = np.arange(-T/2, T/2, 1/fs)                    # Fast-time vector centered at zero
K = B / T                                         # Chirp rate (Hz/s)

# 2. Generate Reference Transmit Chirp & Matched Filter Template
tx_chirp = np.exp(1j * np.pi * K * t**2)          # Complex LFM pulse
h = np.conj(tx_chirp[::-1])                       # Matched filter: time-reversed & complex conjugated

# 3. Simulate Received Signal (Target Return + Noise)
delay_samples = 400                               # Simulates target at a specific range delay
rx_signal = np.pad(tx_chirp, (delay_samples, 200)) # Padded received array
noise = (np.random.randn(len(rx_signal)) + 1j * np.random.randn(len(rx_signal))) * 0.7
rx_noisy = rx_signal + noise                      # Noisy target return

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