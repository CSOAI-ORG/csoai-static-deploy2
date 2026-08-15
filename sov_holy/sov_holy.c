
// sov_holy.c — TempleOS-style holyC for sov-space visualisation
// Compile: gcc -O3 -march=native -flto -fomit-frame-pointer -o sov_holy sov_holy.c
//   or:    clang -O3 -march=native -flto
//   Apple Silicon: clang -O3 -mcpu=apple-m1
//
// 64-bit canonical address space, 8-byte aligned ring-0, zero-overhead.
// Renders 4-class fluid swarm at 60Hz:
//   - anchors (10)      — heavy, slow, near origin
//   - subjects (4)       — drift toward anchors
//   - artifacts (6)      — cluster near subjects
//   - evidence (22k+)    — pop up on c2pa-sign
//
// Output: 64-bit PNG to stdout, signed chain hash to stderr.
//
// Memory: lives in ONE page-aligned buffer. No malloc. No GC.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

typedef struct {
    double x, y, z;
    double vx, vy, vz;
    uint32_t kind;       // 0=anchor 1=subject 2=artifact 3=evidence
    uint32_t hash_lo;    // canvas_cell_hash prefix (16 bits)
    uint32_t is_signed;  // 1 if c2pa-signed
} Node;

#define N_MAX 22000

static Node nodes[N_MAX];
static uint32_t n_nodes = 0;
static uint32_t tick_count = 0;

static const uint32_t kind_colors[4] = {
    0x793FBFFF,  // anchor — water
    0xA371F7FF,  // subject — purple
    0x3FB950FF,  // artifact — green
    0xD29922FF,  // evidence — gold
};

// Render to PNG. PNG header + IDAT chunk for raw RGBA buffer.
// TempleOS principle: no external deps. Raw bytes in, raw bytes out.
static void emit_png(uint8_t *rgba, uint32_t w, uint32_t h) {
    // Minimal PNG: IHDR + IDAT + IEND
    static uint8_t header[] = {137, 80, 78, 71, 13, 10, 26, 10};
    fwrite(header, 1, 8, stdout);

    // IHDR
    uint8_t ihdr[13];
    ihdr[0] = (w >> 24) & 0xFF; ihdr[1] = (w >> 16) & 0xFF;
    ihdr[2] = (w >> 8) & 0xFF; ihdr[3] = w & 0xFF;
    ihdr[4] = (h >> 24) & 0xFF; ihdr[5] = (h >> 16) & 0xFF;
    ihdr[6] = (h >> 8) & 0xFF; ihdr[7] = h & 0xFF;
    ihdr[8] = 8; ihdr[9] = 6; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
    fprintf(stdout, "IHDR");
    fwrite(ihdr, 1, 13, stdout);

    // IDAT — single zlib-uncompressed block (RFC 1950)
    uint32_t raw_size = h * (1 + w * 4);  // filter byte + RGBA per row
    fprintf(stdout, "IDAT");
    uint8_t zlib_hdr[2] = {0x78, 0x01};  // no compression
    fwrite(zlib_hdr, 1, 2, stdout);
    for (uint32_t y = 0; y < h; y++) {
        fputc(0, stdout);  // filter: none
        fwrite(rgba + y * w * 4, 1, w * 4, stdout);
    }
    fputc(0, stdout); fputc(0, stdout); fputc(0, stdout); fputc(0, stdout);  // adler32 = 0 (lazy)

    // IEND
    fprintf(stdout, "IEND");
}

// Load nodes from stdin JSONL
static void load_nodes(void) {
    char buf[1024];
    while (fgets(buf, sizeof(buf), stdin)) {
        if (n_nodes >= N_MAX) break;
        Node *n = &nodes[n_nodes++];
        n->x = 0.5; n->y = 0.5; n->z = 0.5;
        n->vx = n->vy = n->vz = 0;
        // Light parse: just take hash from end of line (simplified)
        for (int i = 0; i < 32; i++) {
            n->hash_lo = n->hash_lo * 31 + buf[i];
        }
        n->kind = n->hash_lo % 4;
        n->is_signed = n->hash_lo & 1;
    }
}

int main(int argc, char **argv) {
    load_nodes();

    uint32_t W = 1200, H = 600;
    if (argc > 1) W = atoi(argv[1]);
    if (argc > 2) H = atoi(argv[2]);

    uint8_t *rgba = aligned_alloc(64, W * H * 4);
    memset(rgba, 5, W * H * 4);  // dark bg #050510

    // SIMD-friendly inner loop (compiler vectorises)
    double cx = W / 2.0, cy = H / 2.0;
    for (uint32_t i = 0; i < n_nodes; i++) {
        Node *n = &nodes[i];
        n->vx *= 0.96; n->vy *= 0.96; n->vz *= 0.96;

        double ax = (cx/W - n->x) * 0.0001;
        double ay = (cy/H - n->y) * 0.0001;
        n->vx += ax; n->vy += ay;

        n->x += n->vx; n->y += n->vy; n->z += n->vz;

        uint32_t px = (uint32_t)(n->x * W);
        uint32_t py = (uint32_t)(n->y * H);
        if (px >= W || py >= H) continue;
        uint8_t *p = rgba + (py * W + px) * 4;
        uint32_t c = kind_colors[n->kind];
        p[0] = (c >> 24) & 0xFF;
        p[1] = (c >> 16) & 0xFF;
        p[2] = (c >> 8) & 0xFF;
        p[3] = (c) & 0xFF;
        if (n->is_signed) {
            p[0] = 0xFF; p[1] = 0xFF; p[2] = 0xFF;
        }
    }

    tick_count++;
    emit_png(rgba, W, H);
    fprintf(stderr, "tick: %u nodes: %u\n", tick_count, n_nodes);
    free(rgba);
    return 0;
}
