# Radar Signal Processing Fundamentals
A personal repository dedicated to exploring and implementing core radar signal processing concepts from scratch.

## Overview
This sandbox project focuses on waveform generation, matched filtering, and performance validation to build intuition around foundational radar engineering math.

## Current Projects
* **1D LFM Pulse Compression & Matched Filtering (`pulse_compression.py`)**
 * Implements a Linear Frequency Modulation (LFM) chirp generator and a custom matched filter.
 * Validates compressed output against theoretical unwindowed peak-to-sidelobe ratio (PSLR) benchmarks (~-13.2 dB).
 * Generates clean `matplotlib` visualizations comparing mainlobe sharpness and sidelobe roll-off.
