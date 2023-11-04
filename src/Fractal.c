#include "Fractal.h"



vector2_double compute_next_julia_double(vector2_double current, vector2_double constant) {
    vector2_double z = new_vector2_double(current.x * current.x - current.y * current.y, 2.0 * current.x * current.y);
    return sum_vector2_double(z, constant);
}

double compute_iterations_julia_double(vector2_double z0, vector2_double constant, int max_iterations) {
    vector2_double zn = z0;
    int iteration = 0;
    
    while((zn.x * zn.x + zn.y * zn.y) < 4.0 && iteration < max_iterations) {
        zn = compute_next_julia_double(zn, constant);
        iteration++;
    }
    
    const double mod = sqrt(zn.x * zn.x + zn.y * zn.y);
    const double smooth = (double)iteration - log2(MAX(1.0, log2(mod)));
    
    return smooth;
}

void *render_thread_julia_double(void *thread_args) {
    struct JuliaDoubleThreadData *data;
    data = (struct JuliaDoubleThreadData *)thread_args;
    
    int x, y;
    for (y = 0; y < data->height; ++y) {
        if (y % data->num_threads == 0 + data->startIndex) {
            for (x = 0; x < data->width; ++x) {
                vector3_float color = new_vector3_float(0.0, 0.0, 0.0);
                double renderScale = 1.0 / data->scale / (double)data->height * 2.5;
                
                int j;
                for (j = data->samples; j != 0; --j) {
                    const double px = ((double)(x - data->width / 2) + _random(-1.0, 1.0)) * renderScale + data->center.x;
                    const double py = ((double)(y - data->height / 2) + _random(-1.0, 1.0)) * renderScale + data->center.y;
                    vector2_double pixel = new_vector2_double(px, py);
                    const double iterations = compute_iterations_julia_double(pixel, data->constant, data->max_iterations);
                    const double value = iterations / data->max_iterations;
                    color = sum_vector3_float(color, get_color_value(value, data->steps, data->num_steps));
                }
                
                pthread_mutex_lock(data->lock);
                set_bitmap_pixel_float(data->bitmap, data->width, x, y, quotient_vector3_float_scalar(color, (float)data->samples));
                pthread_mutex_unlock(data->lock);
            }
        }
    }
    
    return NULL;
}

EMSCRIPTEN_KEEPALIVE void render_julia_double(float *bitmap, int num_threads, int width, int height, struct ColorStep *steps, int num_steps, vector2_double constant, int max_iterations, double scale, int samples, vector2_double center) {
    printf("Rendering julia double...");

    int _num_threads;
    if (num_threads > height) {
        _num_threads = height;
    }
    else if (num_threads <= 0) {
        _num_threads = 1;
    }
    else {
        _num_threads = num_threads;
    }
    
    pthread_mutex_t lock;
    pthread_mutex_init(&lock, NULL);
    pthread_t threads[_num_threads];
    struct JuliaDoubleThreadData thread_data[_num_threads];
    
    int i;
    for (i = 0; i < _num_threads; ++i) {
        struct JuliaDoubleThreadData data;
        data.lock = &lock;
        data.thread_id = threads[i];
        data.num_threads = _num_threads;
        data.startIndex = i;
        data.bitmap = bitmap;
        data.width = width;
        data.height = height;
        data.steps = steps;
        data.num_steps = num_steps;
        data.constant = constant;
        data.max_iterations = max_iterations;
        data.scale = scale;
        data.samples = samples;
        data.center = center;
        
        thread_data[i] = data;
    }
        
    for (i = 0; i < _num_threads; ++i) {
        pthread_create(&threads[i], NULL, &render_thread_julia_double, (void *)&thread_data[i]);
    }
    
    for (i = 0; i < _num_threads; ++i) {
        pthread_join(threads[i], NULL);
    }
    
    pthread_mutex_destroy(&lock);
}



vector2_double compute_next_mandelbrot_double(vector2_double current, vector2_double constant) {
    vector2_double z = new_vector2_double(current.x * current.x - current.y * current.y, 2.0 * current.x * current.y);
    return sum_vector2_double(z, constant);
}

double compute_iterations_mandelbrot_double(vector2_double constant, int max_iterations) {
    vector2_double zn = new_vector2_double(0.0, 0.0);
    int iteration = 0;
    
    while((zn.x * zn.x + zn.y * zn.y) < 4.0 && iteration < max_iterations) {
        zn = compute_next_mandelbrot_double(zn, constant);
        iteration++;
    }
    
    const double mod = sqrt(zn.x * zn.x + zn.y * zn.y);
    const double smooth = (double)iteration - log2(MAX(1.0, log2(mod)));
    
    return smooth;
}

void *render_thread_mandelbrot_double(void *thread_args) {
    struct MandelbrotDoubleThreadData *data;
    data = (struct MandelbrotDoubleThreadData *)thread_args;
    
    int x, y;
    for (y = 0; y < data->height; ++y) {
        if (y % data->num_threads == 0 + data->startIndex) {
            for (x = 0; x < data->width; ++x) {
                vector3_float color = new_vector3_float(0.0, 0.0, 0.0);
                double renderScale = 1.0 / data->scale / (double)data->height * 2.5;
                
                int j;
                for (j = data->samples; j != 0; --j) {
                    const double px = ((double)(x - data->width / 2) + _random(-1.0, 1.0)) * renderScale + data->center.x;
                    const double py = ((double)(y - data->height / 2) + _random(-1.0, 1.0)) * renderScale + data->center.y;
                    vector2_double pixel = new_vector2_double(px, py);
                    const double iterations = compute_iterations_mandelbrot_double(pixel, data->max_iterations);
                    const double valueInv = iterations / data->max_iterations;
                    const double value = 1 - valueInv;
                    color = sum_vector3_float(color, get_color_value(value, data->steps, data->num_steps));
                }
                
                pthread_mutex_lock(data->lock);
                set_bitmap_pixel_float(data->bitmap, data->width, x, y, quotient_vector3_float_scalar(color, (float)data->samples));
                pthread_mutex_unlock(data->lock);
            }
        }
    }
    
    return NULL;
}

EMSCRIPTEN_KEEPALIVE void render_mandelbrot_double(float *bitmap, int num_threads, int width, int height, struct ColorStep *steps, int num_steps, int max_iterations, double scale, int samples, vector2_double center) {

    int _num_threads;
    if (num_threads > height) {
        _num_threads = height;
    }
    else if (num_threads <= 0) {
        _num_threads = 1;
    }
    else {
        _num_threads = num_threads;
    }
    
    pthread_mutex_t lock;
    pthread_mutex_init(&lock, NULL);
    pthread_t threads[_num_threads];
    struct MandelbrotDoubleThreadData thread_data[_num_threads];
    
    int i;
    for (i = 0; i < _num_threads; ++i) {
        struct MandelbrotDoubleThreadData data;
        data.lock = &lock;
        data.thread_id = threads[i];
        data.num_threads = _num_threads;
        data.startIndex = i;
        data.bitmap = bitmap;
        data.width = width;
        data.height = height;
        data.steps = steps;
        data.num_steps = num_steps;
        data.max_iterations = max_iterations;
        data.scale = scale;
        data.samples = samples;
        data.center = center;
        
        thread_data[i] = data;
    }
        
    for (i = 0; i < _num_threads; ++i) {
        pthread_create(&threads[i], NULL, &render_thread_mandelbrot_double, (void *)&thread_data[i]);
    }
    
    for (i = 0; i < _num_threads; ++i) {
        pthread_join(threads[i], NULL);
    }
    
    pthread_mutex_destroy(&lock);
}




double _random(double min, double max) {
    double n = (double)rand() / RAND_MAX;
    return min + n * (max - min);
}

vector3_float get_color_value(float value, struct ColorStep *steps, int num_steps) {
    vector3_float color_value;
    if (value >= 1.0) {
        color_value = steps[num_steps - 1].rgb;
        return color_value;
    } else if (value <= 0.0) {
        color_value = steps[0].rgb;
        return color_value;
    }

    int i;
    for (i = 0; i < num_steps; ++i) {
        if (steps[i].value > value) {
            const float range = steps[i].value - steps[i - 1].value;
            const float pos = value - steps[i - 1].value;
            const float ratio = pos / range;
            vector3_float a = product_vector3_float_scalar(steps[i - 1].rgb, (1.0 - ratio));
            vector3_float b = product_vector3_float_scalar(steps[i].rgb, ratio);
            vector3_float result = sum_vector3_float(a, b);
            color_value = new_vector3_float(result.x, result.y, result.z);

            return color_value;
        }
    }
    
    color_value = new_vector3_float(0.0, 0.0, 0.0);
    return color_value;
}

void set_bitmap_pixel_float(float *bitmap, int width, int x, int y, vector3_float color) {
    bitmap[y * width * 3 + x * 3 + 0] = color.x;
    bitmap[y * width * 3 + x * 3 + 1] = color.y;
    bitmap[y * width * 3 + x * 3 + 2] = color.z;
}
