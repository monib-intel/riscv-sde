/**
 * Fast Fourier Transform (FFT) Implementation for RISC-V
 * 
 * This file contains a radix-2 decimation-in-time FFT implementation
 * optimized for RISC-V processors.
 */

#include <stdint.h>
#include <math.h>
#include <complex.h>
#include "../common/profiling.h"

// Define complex number type for FFT
typedef float complex cmplx;

/**
 * Bit-reversal permutation for FFT input
 * 
 * @param input Input array of complex numbers
 * @param output Output array of bit-reversed order
 * @param n Size of the array (must be power of 2)
 */
void bit_reverse_permutation(cmplx *input, cmplx *output, int n) {
    // Initialize profiling
    PROFILE_START("bit_reverse");
    
    int bits = (int)log2f(n);
    
    // Perform bit reversal
    for (int i = 0; i < n; i++) {
        int rev = 0;
        for (int j = 0; j < bits; j++) {
            if (i & (1 << j))
                rev |= (1 << (bits - 1 - j));
        }
        output[rev] = input[i];
    }
    
    PROFILE_END("bit_reverse");
}

/**
 * Radix-2 decimation-in-time FFT implementation
 * 
 * @param input Input array of complex numbers (will be modified in-place)
 * @param n Size of the array (must be power of 2)
 */
void fft_radix2(cmplx *input, int n) {
    // Initialize profiling
    PROFILE_START("fft_computation");
    
    // Base case
    if (n <= 1) {
        PROFILE_END("fft_computation");
        return;
    }
    
    // Allocate arrays for even and odd elements
    cmplx even[n/2];
    cmplx odd[n/2];
    
    // Split input into even and odd elements
    for (int i = 0; i < n/2; i++) {
        even[i] = input[2*i];
        odd[i] = input[2*i + 1];
    }
    
    // Recursively compute FFT of even and odd elements
    fft_radix2(even, n/2);
    fft_radix2(odd, n/2);
    
    // Combine results
    for (int k = 0; k < n/2; k++) {
        // Twiddle factor
        float angle = -2.0f * M_PI * k / n;
        cmplx twiddle = cosf(angle) + sinf(angle) * I;
        
        cmplx t = twiddle * odd[k];
        input[k] = even[k] + t;
        input[k + n/2] = even[k] - t;
    }
    
    PROFILE_END("fft_computation");
}

/**
 * Main FFT function with bit-reversal and in-place computation
 * 
 * @param input Input array of complex numbers
 * @param output Output array for FFT result
 * @param n Size of the array (must be power of 2)
 */
void fft(cmplx *input, cmplx *output, int n) {
    PROFILE_INIT();
    PROFILE_START("fft_total");
    
    // Perform bit-reversal permutation
    bit_reverse_permutation(input, output, n);
    
    // Perform in-place FFT
    fft_radix2(output, n);
    
    PROFILE_END("fft_total");
    PROFILE_REPORT();
}

/**
 * Entry point when compiled as standalone executable
 */
int main() {
    // Example FFT of size 16
    const int N = 16;
    cmplx input[N];
    cmplx output[N];
    
    // Initialize input with a simple signal
    for (int i = 0; i < N; i++) {
        // Create a signal with a few frequency components
        input[i] = cosf(2.0f * M_PI * i / N) + 0.5f * cosf(4.0f * M_PI * i / N) * I;
    }
    
    // Perform FFT
    fft(input, output, N);
    
    // Print results (for verification)
    for (int i = 0; i < N; i++) {
        printf("%d: %f + %fi\n", i, crealf(output[i]), cimagf(output[i]));
    }
    
    return 0;
}
