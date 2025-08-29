/**
 * SHA-256 Implementation for RISC-V
 * 
 * This file contains a SHA-256 hash implementation
 * optimized for RISC-V processors.
 */

#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include "../common/profiling.h"

// SHA-256 constants
#define SHA256_BLOCK_SIZE 64
#define SHA256_DIGEST_SIZE 32

// SHA-256 initial hash values (first 32 bits of the fractional parts of the square roots of the first 8 primes)
static const uint32_t H0[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

// SHA-256 round constants (first 32 bits of the fractional parts of the cube roots of the first 64 primes)
static const uint32_t K[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

// SHA-256 functions
#define ROTR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22))
#define EP1(x) (ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25))
#define SIG0(x) (ROTR(x, 7) ^ ROTR(x, 18) ^ ((x) >> 3))
#define SIG1(x) (ROTR(x, 17) ^ ROTR(x, 19) ^ ((x) >> 10))

// SHA-256 state
typedef struct {
    uint32_t h[8];           // Hash state
    uint8_t data[64];        // Input data buffer
    uint64_t datalen;        // Length of input data in bytes
    uint64_t bitlen;         // Length of message in bits
} SHA256_CTX;

/**
 * Initialize SHA-256 context
 */
void sha256_init(SHA256_CTX *ctx) {
    ctx->datalen = 0;
    ctx->bitlen = 0;
    memcpy(ctx->h, H0, 32);
}

/**
 * Process a single block of data
 */
void sha256_transform(SHA256_CTX *ctx, const uint8_t data[]) {
    uint32_t a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];
    
    // Prepare message schedule
    for (i = 0, j = 0; i < 16; ++i, j += 4) {
        m[i] = ((uint32_t)data[j] << 24) | ((uint32_t)data[j + 1] << 16) |
               ((uint32_t)data[j + 2] << 8) | ((uint32_t)data[j + 3]);
    }
    for (; i < 64; ++i) {
        m[i] = SIG1(m[i - 2]) + m[i - 7] + SIG0(m[i - 15]) + m[i - 16];
    }
    
    // Initialize working variables
    a = ctx->h[0];
    b = ctx->h[1];
    c = ctx->h[2];
    d = ctx->h[3];
    e = ctx->h[4];
    f = ctx->h[5];
    g = ctx->h[6];
    h = ctx->h[7];
    
    // Main loop
    for (i = 0; i < 64; ++i) {
        t1 = h + EP1(e) + CH(e, f, g) + K[i] + m[i];
        t2 = EP0(a) + MAJ(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + t1;
        d = c;
        c = b;
        b = a;
        a = t1 + t2;
    }
    
    // Update hash state
    ctx->h[0] += a;
    ctx->h[1] += b;
    ctx->h[2] += c;
    ctx->h[3] += d;
    ctx->h[4] += e;
    ctx->h[5] += f;
    ctx->h[6] += g;
    ctx->h[7] += h;
}

/**
 * Update SHA-256 context with input data
 */
void sha256_update(SHA256_CTX *ctx, const uint8_t data[], size_t len) {
    uint32_t i;
    
    for (i = 0; i < len; ++i) {
        ctx->data[ctx->datalen] = data[i];
        ctx->datalen++;
        if (ctx->datalen == 64) {
            sha256_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}

/**
 * Finalize SHA-256 hash computation and output the result
 */
void sha256_final(SHA256_CTX *ctx, uint8_t hash[]) {
    uint32_t i;
    
    i = ctx->datalen;
    
    // Pad the message
    if (ctx->datalen < 56) {
        ctx->data[i++] = 0x80; // Append 1 bit
        while (i < 56) {
            ctx->data[i++] = 0x00; // Pad with zeros
        }
    } else {
        ctx->data[i++] = 0x80; // Append 1 bit
        while (i < 64) {
            ctx->data[i++] = 0x00; // Pad with zeros
        }
        sha256_transform(ctx, ctx->data);
        memset(ctx->data, 0, 56);
    }
    
    // Append length in bits
    ctx->bitlen += ctx->datalen * 8;
    ctx->data[63] = (uint8_t)ctx->bitlen;
    ctx->data[62] = (uint8_t)(ctx->bitlen >> 8);
    ctx->data[61] = (uint8_t)(ctx->bitlen >> 16);
    ctx->data[60] = (uint8_t)(ctx->bitlen >> 24);
    ctx->data[59] = (uint8_t)(ctx->bitlen >> 32);
    ctx->data[58] = (uint8_t)(ctx->bitlen >> 40);
    ctx->data[57] = (uint8_t)(ctx->bitlen >> 48);
    ctx->data[56] = (uint8_t)(ctx->bitlen >> 56);
    sha256_transform(ctx, ctx->data);
    
    // Output hash
    for (i = 0; i < 8; ++i) {
        hash[i * 4] = (uint8_t)(ctx->h[i] >> 24);
        hash[i * 4 + 1] = (uint8_t)(ctx->h[i] >> 16);
        hash[i * 4 + 2] = (uint8_t)(ctx->h[i] >> 8);
        hash[i * 4 + 3] = (uint8_t)ctx->h[i];
    }
}

/**
 * Complete SHA-256 hash in one function call
 */
void sha256(const uint8_t data[], size_t len, uint8_t hash[]) {
    PROFILE_START("sha256");
    
    SHA256_CTX ctx;
    sha256_init(&ctx);
    sha256_update(&ctx, data, len);
    sha256_final(&ctx, hash);
    
    PROFILE_END("sha256");
}

/**
 * Entry point when compiled as standalone executable
 */
int main() {
    // Initialize profiling
    PROFILE_INIT();
    
    // Test vector
    const char *test = "Hello, RISC-V!";
    uint8_t hash[SHA256_DIGEST_SIZE];
    
    // Compute hash
    sha256((const uint8_t *)test, strlen(test), hash);
    
    // Print result
    printf("SHA-256(\"%s\") = ", test);
    for (int i = 0; i < SHA256_DIGEST_SIZE; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
    
    // Output profiling results
    PROFILE_REPORT();
    
    return 0;
}
