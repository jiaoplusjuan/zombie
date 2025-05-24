// This file contains helper functions for reading and writing images in PNG and
// PFM format.

#pragma once

#include <Eigen/Core>
#include <Eigen/Geometry>
#include <algorithm>
#include <array>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

template <size_t DIM>
using Array = Eigen::Array<float, DIM, 1>;
using Array3 = Array<3>;
using Vector2 = Eigen::Matrix<float, 2, 1>;
using Vector2i = Eigen::Matrix<int, 2, 1>;

using Vector3 = Eigen::Matrix<float, 3, 1>;
using Vector3i = Eigen::Matrix<int, 3, 1>;