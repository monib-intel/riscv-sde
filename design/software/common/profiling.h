/**
 * Common profiling utilities for benchmarks
 */

#ifndef PROFILING_H
#define PROFILING_H

#include <stdint.h>
#include <stdio.h>
#include <string.h>

// Configuration
#define MAX_TIMERS 32
#define MAX_TIMER_NAME 64

// Timer storage
typedef struct {
    char name[MAX_TIMER_NAME];
    uint64_t start;
    uint64_t end;
    uint64_t elapsed;
    int active;
} profile_timer_t;

// Global timer state
static profile_timer_t timers[MAX_TIMERS];
static int num_timers = 0;
static int profiling_initialized = 0;

/**
 * Initialize profiling system
 */
#define PROFILE_INIT() do { \
    if (!profiling_initialized) { \
        memset(timers, 0, sizeof(timers)); \
        num_timers = 0; \
        profiling_initialized = 1; \
    } \
} while (0)

/**
 * Get current cycle count
 */
static inline uint64_t get_cycles() {
    uint64_t cycles;
    #if defined(__riscv)
    // RISC-V cycle counter
    asm volatile ("rdcycle %0" : "=r" (cycles));
    #else
    // Fallback for non-RISC-V platforms (e.g., x86)
    // This is just a placeholder and not accurate
    static uint64_t counter = 0;
    cycles = counter++;
    #endif
    return cycles;
}

/**
 * Start a named timer
 */
#define PROFILE_START(name) do { \
    if (!profiling_initialized) PROFILE_INIT(); \
    int idx = -1; \
    for (int i = 0; i < num_timers; i++) { \
        if (strcmp(timers[i].name, name) == 0) { \
            idx = i; \
            break; \
        } \
    } \
    if (idx == -1) { \
        idx = num_timers++; \
        strncpy(timers[idx].name, name, MAX_TIMER_NAME-1); \
        timers[idx].name[MAX_TIMER_NAME-1] = '\0'; \
        timers[idx].elapsed = 0; \
    } \
    timers[idx].start = get_cycles(); \
    timers[idx].active = 1; \
} while (0)

/**
 * End a named timer
 */
#define PROFILE_END(name) do { \
    if (!profiling_initialized) return; \
    int idx = -1; \
    for (int i = 0; i < num_timers; i++) { \
        if (strcmp(timers[i].name, name) == 0) { \
            idx = i; \
            break; \
        } \
    } \
    if (idx != -1 && timers[idx].active) { \
        timers[idx].end = get_cycles(); \
        timers[idx].elapsed += timers[idx].end - timers[idx].start; \
        timers[idx].active = 0; \
    } \
} while (0)

/**
 * Report profiling results
 */
#define PROFILE_REPORT() do { \
    printf("===== Profiling Report =====\n"); \
    for (int i = 0; i < num_timers; i++) { \
        printf("%-20s: %lu cycles\n", timers[i].name, timers[i].elapsed); \
    } \
    printf("===========================\n"); \
} while (0)

#endif /* PROFILING_H */
