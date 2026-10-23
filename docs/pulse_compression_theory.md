# Fundamentals of Radar Signal Processing: Pulse Compression & Baseband Architectures

## 1. The Physics of Time and Space (Seconds to Meters)

* **The Conversion Factor:** Radio waves travel at the speed of light ($\c \approx 3 \times 10^8\$ m/s), which translates to exactly **300 meters per microsecond** in the air.
* **The Absolute Range Equation:** To find the distance to a single target, we map the round-trip time delay ($\tau\$) to space. We divide by 2 because the signal travels out and back:
$\[R = \frac{c \cdot \tau}{2}\$]
* **The Range Resolution ($\Delta R\$) Constraint:** For an unmodulated (pure) pulse, the radar can only separate two targets if their echoes do not overlap in time. Because the pulse must traverse the physical gap between targets twice (out and back), the structural resolution limit of an unmodulated pulse is:
$$\[\Delta R = \frac{c \cdot \tau}{2}\$$]
*Example:* A **10 μs** unmodulated pulse physically spans **3 km** in the air. Without modulation, your range resolution is stuck at a massive **1.5 km**.

---

## 2. Linear Frequency Modulation (LFM) Chirp Waves

* **The Structure:** An LFM chirp is a single, gated burst of energy where the frequency changes linearly over the duration of the pulse.
* **The Slope Equation:** The rate at which the frequency sweeps is defined by the chirp rate, **K**:
$\[K = \frac{B}{T}\$]
Where \(B\) is the modulation bandwidth and \(T\) is the pulse duration.
*Example:* Sweeping a **20 MHz** bandwidth over a **10 μs** pulse means the frequency accelerates at a rate of **2 MHz per microsecond** ($\(2 \times 10^{12}\$) Hz/s).
* **The Purpose:** By adding bandwidth, every individual slice of the pulse gets a unique frequency signature. This allows the receiver to bypass the physical pulse-width restriction, collapsing a long pulse down to a compressed range resolution determined solely by bandwidth:
$\[\Delta R = \frac{c}{2B}\$]
This shrinks the 1.5 km limit down to just **7.5 meters** using the parameters above.

---

## 3. Symmetrical Baseband Processing & Time Centering

* **Zero-Centered Time Vectors:** Defining the pulse vector locally from $\(-T/2\) to \(+T/2\$) places $\(t = 0\$) perfectly in the middle of the pulse.
* **Mathematical Symmetries:** Centering time forces the instantaneous phase function (\(\phi(t) = \pi K t^2\)) to be symmetric around zero:
  * **Real Part (I Channel):** $\(\cos(\pi K t^2)\$) becomes a perfectly **even function** ($\(f(t) = f(-t)\$)).
  * **Imaginary Part (Q Channel):** $\(\sin(\pi K t^2)\$) becomes a perfectly **odd function** ($\(f(-t) = -f(t)\$)).
* **Fourier Impact:** In Fourier theory, a signal with an even real component and an odd imaginary component yields a **purely real-valued frequency spectrum**. This symmetry removes messy linear phase ramps, preventing artificial phase-wrapping distortions when processing data matrices.
* **Baseband:** Baseband refers to the raw signal shifted down to sit symmetrically around **0 Hz**. Operating at baseband means our 20 MHz chirp sweeps cleanly from -10 MHz to +10 MHz ($\(-B/2\) to \(+B/2\$)).

---

## 4. Direct Conversion Hardware & Slower ADCs

* **The I/Q Demodulator Circuit:** The physical radar hardware strips away the high-frequency RF carrier wave (e.g., 10 GHz) using **analog frequency mixers**. The incoming echo is multiplied by an internal Local Oscillator reference tone ($\(\cos\$)) and a 90-degree phase-shifted version ($\(\sin\$)).
* **Frequency Subtraction:** Multiplication physically generates sum and difference frequencies. The high-frequency sums are filtered out, leaving the difference frequency ($\(\text{Signal} - \text{Carrier}\$)), which drops the spectrum right down to the centered baseband window.
* **The Complex Nyquist Rate:** For a real-valued signal, the sampling rate must be $\(2 \times f_{\max}\$). But because complex I/Q sampling tracks two independent dimensions simultaneously, the complex Nyquist boundary drops to exactly equal the bandwidth ($\(f_s = B\$)).
* **Hardware Advantage:** By centering the spectrum at $\(\pm B/2\$), the maximum frequency component drops to 10 MHz. The system routes the signal into **two slower, parallel ADCs** running at 20 MHz rather than forcing a single, expensive real-valued ADC to run at 40 MHz. Slower ADC clocks provide higher dynamic range, less thermal noise, and lower component costs.

---

## 5. Matched Filtering & Convolution Math

* **The Code Implementation:** The optimal receiver filter is built by time-reversing and complex-conjugating the transmitted chirp:
```python
h = np.conj(tx_chirp[::-1])
```
* **Convolution ($\ast$) vs. Correlation:** Linear system theory dictates that filtering happens via convolution, which inherently flips the filter array in time ($-\tau$). The slicing syntax **`[::-1]`** pre-flips our template so that the convolution engine flips it back into its correct forward-facing orientation. This ensures the frequency sweep profiles align perfectly as they slide across one another.
* **Phase Flattening:** The complex conjugate (`np.conj()`) flips the sign of the imaginary channel. When the incoming reflection meets this conjugated filter, their phases subtract:
$$ \exp(j \pi K t^2) \times \exp(-j \pi K t^2) = \exp(j0) = 1 $$
This flattens the rapidly wrapping phase across the entire 10 μs window. Instead of canceling itself out, the energy across all samples sums constructively, transforming a wide, low-amplitude return into a sharp, high-intensity range spike.

---

## 6. What is Pulse Compression in this Context?

In a functional radar script, pulse compression is the mathematical conversion of a long, low-power spatial smear of energy into a single, localized, high-SNR tracking spike:
* **Energy Concentrator:** The raw target reflection is spread across 1,000 digitized data samples (10 μs duration $\times$ 100 MHz sampling rate). The matched filter gathers the scattered phase energy across all 1,000 bins and packs it into a single high-amplitude sample spike at index 400.
* **SNR Booster:** White noise is completely uncorrelated and cannot compress, so the noise floor remains flat. The structured target phase, however, perfectly matches the filter template. This creates a massive power amplification (Processing Gain) at the peak, pulling weak echoes out from under the noise floor.
* **Resolution Liberator:** It unties radar resolution from pulse duration. It allows the system to use long pulses to send high energy out into space (for maximum range tracking), while maintaining the tight, razor-sharp range resolution (7.5 meters) typically only possible with short pulses.
