#ifndef Simd_h
#define Simd_h

#include <stdio.h>
#include <math.h>

typedef struct {
    double x;
    double y;
} vector2_double;

vector2_double new_vector2_double(double x, double y);
vector2_double sum_vector2_double(vector2_double x, vector2_double y);
vector2_double sum_vector2_double_scalar(vector2_double x, double y);

typedef struct {
    float x;
    float y;
    float z;
} vector3_float;

vector3_float new_vector3_float(float x, float y, float z);
vector3_float sum_vector3_float(vector3_float x, vector3_float y);
vector3_float quotient_vector3_float_scalar(vector3_float x, float y);
vector3_float product_vector3_float_scalar(vector3_float x, float y);

#endif