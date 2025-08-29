/**
 * Matrix Multiplication Implementation for RISC-V
 * 
 * This file contains different matrix multiplication implementations
 * optimized for RISC-V processors.
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "../common/profiling.h"

/**
 * Basic matrix multiplication (A x B = C)
 * 
 * @param A First input matrix (M x K)
 * @param B Second input matrix (K x N)
 * @param C Output matrix (M x N)
 * @param M Number of rows in A
 * @param K Number of columns in A / rows in B
 * @param N Number of columns in B
 */
void matrix_multiply_basic(float *A, float *B, float *C, int M, int K, int N) {
    PROFILE_START("matmul_basic");
    
    // Initialize output matrix to zeros
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            C[i*N + j] = 0.0f;
        }
    }
    
    // Standard matrix multiplication
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < K; k++) {
                C[i*N + j] += A[i*K + k] * B[k*N + j];
            }
        }
    }
    
    PROFILE_END("matmul_basic");
}

/**
 * Blocked matrix multiplication for better cache utilization
 * 
 * @param A First input matrix (M x K)
 * @param B Second input matrix (K x N)
 * @param C Output matrix (M x N)
 * @param M Number of rows in A
 * @param K Number of columns in A / rows in B
 * @param N Number of columns in B
 * @param block_size Block size for tiling
 */
void matrix_multiply_blocked(float *A, float *B, float *C, int M, int K, int N, int block_size) {
    PROFILE_START("matmul_blocked");
    
    // Initialize output matrix to zeros
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            C[i*N + j] = 0.0f;
        }
    }
    
    // Blocked matrix multiplication
    for (int i0 = 0; i0 < M; i0 += block_size) {
        for (int j0 = 0; j0 < N; j0 += block_size) {
            for (int k0 = 0; k0 < K; k0 += block_size) {
                // Process one block
                for (int i = i0; i < i0 + block_size && i < M; i++) {
                    for (int j = j0; j < j0 + block_size && j < N; j++) {
                        float sum = C[i*N + j];
                        for (int k = k0; k < k0 + block_size && k < K; k++) {
                            sum += A[i*K + k] * B[k*N + j];
                        }
                        C[i*N + j] = sum;
                    }
                }
            }
        }
    }
    
    PROFILE_END("matmul_blocked");
}

/**
 * Entry point when compiled as standalone executable
 */
int main() {
    // Initialize profiling
    PROFILE_INIT();
    
    // Test matrix sizes
    const int M = 64;
    const int K = 64;
    const int N = 64;
    const int block_size = 16;
    
    // Allocate matrices
    float *A = (float *)malloc(M * K * sizeof(float));
    float *B = (float *)malloc(K * N * sizeof(float));
    float *C1 = (float *)malloc(M * N * sizeof(float));
    float *C2 = (float *)malloc(M * N * sizeof(float));
    
    // Initialize input matrices with some values
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < K; j++) {
            A[i*K + j] = (float)(i + j) / (M + K);
        }
    }
    
    for (int i = 0; i < K; i++) {
        for (int j = 0; j < N; j++) {
            B[i*N + j] = (float)(i * j) / (K * N);
        }
    }
    
    // Run basic matrix multiplication
    matrix_multiply_basic(A, B, C1, M, K, N);
    
    // Run blocked matrix multiplication
    matrix_multiply_blocked(A, B, C2, M, K, N, block_size);
    
    // Verify results
    float max_diff = 0.0f;
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            float diff = fabsf(C1[i*N + j] - C2[i*N + j]);
            if (diff > max_diff) {
                max_diff = diff;
            }
        }
    }
    
    printf("Maximum difference between basic and blocked implementations: %e\n", max_diff);
    
    // Output profiling results
    PROFILE_REPORT();
    
    // Free memory
    free(A);
    free(B);
    free(C1);
    free(C2);
    
    return 0;
}
