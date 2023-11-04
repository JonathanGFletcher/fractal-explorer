#ifndef Fractal_h
#define Fractal_h

#define MIN(x, y) (((x) < (y)) ? (x) : (y))
#define MAX(x, y) (((x) > (y)) ? (x) : (y))

#include "Simd.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include <emscripten.h>



struct ColorStep {
    float value;
    vector3_float rgb;
};

struct JuliaDoubleThreadData {
    pthread_mutex_t *lock;
    pthread_t thread_id;
    int num_threads;
    int startIndex;
    float *bitmap;
    int width;
    int height;
    struct ColorStep *steps;
    int num_steps;
    vector2_double constant;
    int max_iterations;
    double scale;
    int samples;
    vector2_double center;
};

struct MandelbrotDoubleThreadData {
    pthread_mutex_t *lock;
    pthread_t thread_id;
    int num_threads;
    int startIndex;
    float *bitmap;
    int width;
    int height;
    struct ColorStep *steps;
    int num_steps;
    int max_iterations;
    double scale;
    int samples;
    vector2_double center;
};



// Julia Double
vector2_double compute_next_julia_double(vector2_double current, vector2_double constant);
double compute_iterations_julia_double(vector2_double z0, vector2_double constant, int max_iterations);
void *render_thread_julia_double(void *thread_args);
EMSCRIPTEN_KEEPALIVE void render_julia_double(float *bitmap, int num_threads, int width, int height, struct ColorStep *steps, int num_steps, vector2_double constant, int max_iterations, double scale, int samples, vector2_double center);

// Mandelbrot Double
vector2_double compute_next_mandelbrot_double(vector2_double current, vector2_double constant);
double compute_iterations_mandelbrot_double(vector2_double constant, int max_iterations);
void *render_thread_mandelbrot_double(void *thread_args);
EMSCRIPTEN_KEEPALIVE void render_mandelbrot_double(float *bitmap, int num_threads, int width, int height, struct ColorStep *steps, int num_steps, int max_iterations, double scale, int samples, vector2_double center);


double _random(double min, double max);
vector3_float get_color_value(float value, struct ColorStep *steps, int num_steps);
void set_bitmap_pixel_float(float *bitmap, int width, int x, int y, vector3_float);

#endif