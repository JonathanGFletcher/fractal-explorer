#include "Simd.h"

vector2_double new_vector2_double(double x, double y) {
    vector2_double v;
    v.x = x;
    v.y = y;
    return v;
}

vector2_double sum_vector2_double(vector2_double x, vector2_double y) {
    vector2_double v;
    v.x = x.x + y.x;
    v.y = x.y + y.y;
    return v;
}

vector2_double sum_vector2_double_scalar(vector2_double x, double y) {
    vector2_double v;
    v.x = x.x + y;
    v.y = x.y + y;
    return v;
}

vector3_float new_vector3_float(float x, float y, float z) {
    vector3_float v;
    v.x = x;
    v.y = y;
    v.z = z;
    return v;
}

vector3_float sum_vector3_float(vector3_float x, vector3_float y) {
    vector3_float v;
    v.x = x.x + y.x;
    v.y = x.y + y.y;
    v.z = x.z + y.z;
    return v;
}

vector3_float quotient_vector3_float_scalar(vector3_float x, float y) {
    vector3_float v;
    v.x = x.x / y;
    v.y = x.y / y;
    v.z = x.z / y;
    return v;
}

vector3_float product_vector3_float_scalar(vector3_float x, float y) {
    vector3_float v;
    v.x = x.x * y;
    v.y = x.y * y;
    v.z = x.z * y;
    return v;
}