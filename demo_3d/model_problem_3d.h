// This file defines a ModelProblem class, which is used to describe a
// scalar-valued Poisson or screened Poisson PDE on a 3D domain via a boundary
// mesh, associated boundary conditions, source term, and robin and absorption
// coefficients.
//
// The boundary mesh is read from an OBJ file, while the input PDE data is read
// from images for the purposes of this demo. NOTE: Users may analogously define
// a ModelProblem class for 3D domains and/or vector-valued PDEs, as all
// functionality in Zombie is templated on the dimension and value type of the
// PDE.

#pragma once

#include <zombie/zombie.h>
#include <fstream>
#include <sstream>
#include "config.h"
// #include "image.h"
#include "3d.h"
#include "unistd.h"

class ModelProblem {
   public:
    // constructor
    ModelProblem(const json& config, std::string directoryPath);

    // members
    bool solveDoubleSided;
    std::vector<Vector3i> indices;
    std::vector<Vector3i> absorbingBoundaryIndices;
    std::vector<Vector3i> reflectingBoundaryIndices;
    std::vector<Vector3> positions;
    std::vector<Vector3> absorbingBoundaryPositions;
    std::vector<Vector3> reflectingBoundaryPositions;
    std::pair<Vector3, Vector3> boundingBox;
    zombie::PDE<float, 3> pde;
    zombie::GeometricQueries<3> queries;

   protected:
    // loads a boundary mesh from an OBJ file
    void loadOBJ(const std::string& filename,
                 bool normalize,
                 bool flipOrientation);

    // sets up the PDE
    void setupPDE();

    // partitions the boundary mesh into absorbing and reflecting parts
    void partitionBoundaryMesh();

    // populates geometric queries for the absorbing and reflecting boundary
    void populateGeometricQueries();

    // members
    // Image<1> isReflectingBoundary;
    // Image<1> absorbingBoundaryValue;
    // Image<1> reflectingBoundaryValue;
    // Image<1> sourceValue;
    bool domainIsWatertight;
    bool useSdfForAbsorbingBoundary;
    int sdfGridResolution;
    float robinCoeff, absorptionCoeff;
    std::vector<float> minRobinCoeffValues;
    std::vector<float> maxRobinCoeffValues;
    std::unique_ptr<zombie::SdfGrid<3>> sdfGridForAbsorbingBoundary;
    zombie::FcpwDirichletBoundaryHandler<3> absorbingBoundaryHandler;
    zombie::FcpwNeumannBoundaryHandler<3> reflectingNeumannBoundaryHandler;
    zombie::FcpwRobinBoundaryHandler<3> reflectingRobinBoundaryHandler;
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation

ModelProblem::ModelProblem(const json& config, std::string directoryPath)
    : sdfGridForAbsorbingBoundary(nullptr) {
    // load config settings
    std::string geometryFile =
        directoryPath + getRequired<std::string>(config, "geometry");
    bool normalize = getOptional<bool>(config, "normalizeDomain", true);
    bool flipOrientation = getOptional<bool>(config, "flipOrientation", true);
    // isReflectingBoundary =
    //     Image<1>(directoryPath +
    //              getRequired<std::string>(config, "isReflectingBoundary"));
    // absorbingBoundaryValue =
    //     Image<1>(directoryPath +
    //              getRequired<std::string>(config, "absorbingBoundaryValue"));
    // reflectingBoundaryValue =
    //     Image<1>(directoryPath +
    //              getRequired<std::string>(config, "reflectingBoundaryValue"));
    // sourceValue = Image<1>(directoryPath +
    //                        getRequired<std::string>(config, "sourceValue"));
    solveDoubleSided = getOptional<bool>(config, "solveDoubleSided", false);
    domainIsWatertight = getOptional<bool>(config, "domainIsWatertight", true);
    useSdfForAbsorbingBoundary =
        getOptional<bool>(config, "useSdfForAbsorbingBoundary", false);
    sdfGridResolution = getOptional<int>(config, "sdfGridResolution", 138);
    robinCoeff = getOptional<float>(config, "robinCoeff", 0.0f);
    absorptionCoeff = getOptional<float>(config, "absorptionCoeff", 0.0f);

    // load a boundary mesh from an OBJ file
    loadOBJ(geometryFile, normalize, flipOrientation);
    std::cout << "loaded " << positions.size() << " vertices and "
              << indices.size() << " triangles" << std::endl;
    std::cout << "vertex positions: " << std::endl;
    for (const auto& p : positions) {
        std::cout << p.transpose() << std::endl;
    }
    std::cout << "triangle indices: " << std::endl;
    for (const auto& t : indices) {
        std::cout << t.transpose() << std::endl;
    }

    // setup the PDE
    setupPDE();

    // partition the boundary mesh into absorbing and reflecting boundary
    // elements
    partitionBoundaryMesh();

    // specify the minimum and maximum Robin coefficient values for each
    // reflecting boundary element: we use a constant value for all elements in
    // this demo, but Zombie supports variable coefficients
    minRobinCoeffValues.resize(reflectingBoundaryIndices.size(),
                               std::fabs(robinCoeff));
    maxRobinCoeffValues.resize(reflectingBoundaryIndices.size(),
                               std::fabs(robinCoeff));

    // populate the geometric queries for the absorbing and reflecting boundary
    populateGeometricQueries();
}

void ModelProblem::loadOBJ(const std::string& filename,
                           bool normalize,
                           bool flipOrientation) {
    zombie::loadBoundaryMesh<3>(filename, positions, indices);
    if (normalize)
        zombie::normalize<3>(positions);
    if (flipOrientation)
        zombie::flipOrientation<3>(indices);
    boundingBox = zombie::computeBoundingBox<3>(positions, true, 1.0);
}

void ModelProblem::setupPDE() {
    Vector3 bMin = boundingBox.first;
    Vector3 bMax = boundingBox.second;
    float maxLength = (bMax - bMin).maxCoeff();
    std::cout << bMin << " " << maxLength << " " << bMax << std::endl;

    pde.source = [this, bMin, maxLength](const Vector3& x) -> float {
        // Vector3 uv = (x - bMin) / maxLength;
        // return this->sourceValue.get(uv)[0];
        std::cout << "source: " << x << std::endl;
        return 0.0f;
    };
    // pde.dirichlet = [this, bMin, bMax, maxLength](const Vector3& x, //
    // TODO 渐变立方体
    //                                               bool _) -> float {
    //     Vector3 uv = (x - bMin) / maxLength;
    //     float max_uv = std::max(std::max(uv[0], uv[1]), uv[2]);
    //     float min_uv = std::min(std::min(uv[0], uv[1]), uv[2]);

    //     bool uv_on_x = (uv[0] < 1e-4) ||
    //                    (uv[0] > ((bMax[0] - bMin[0]) / maxLength - 1e-4));
    //     bool uv_on_y = (uv[1] < 1e-4) ||
    //                    (uv[1] > ((bMax[1] - bMin[1]) / maxLength - 1e-4));
    //     bool uv_on_z = (uv[2] < 1e-4) ||
    //                    (uv[2] > ((bMax[2] - bMin[2]) / maxLength - 1e-4));
    //     float dist_to_max = (bMax - x).norm();

    //     if (uv_on_x || uv_on_y || uv_on_z) {
    //         return dist_to_max;
    //     }
    //     return 0.0f;
    // };
    pde.dirichlet = [this, bMin, bMax](const Vector3& x,
                                       bool _) -> float {  // TODO 空洞立方体
        // 拉长的小立方体范围（x 方向拉长，y 和 z 方向尺寸 1.0）
        float hole_x_min = -0.8f;
        float hole_x_max = 0.8f;
        float hole_y_min = -0.5f;
        float hole_y_max = 0.5f;
        float hole_z_min = -0.5f;
        float hole_z_max = 0.5f;

        // 判断是否在小立方体内
        bool inside_hole = (x[0] >= hole_x_min && x[0] <= hole_x_max) &&
                           (x[1] >= hole_y_min && x[1] <= hole_y_max) &&
                           (x[2] >= hole_z_min && x[2] <= hole_z_max);
        float dist_to_max = (bMax - x).norm();
        float dist_to_min = (bMin - x).norm();

        if (inside_hole) {
            return 0.0f;  // 洞区域返回 0
        }

        // 判断是否在大立方体的边界上
        bool on_outer_boundary =
            (x[0] <= bMin[0] + 1e-4) || (x[0] >= bMax[0] - 1e-4) ||
            (x[1] <= bMin[1] + 1e-4) || (x[1] >= bMax[1] - 1e-4) ||
            (x[2] <= bMin[2] + 1e-4) || (x[2] >= bMax[2] - 1e-4);

        if (on_outer_boundary) {
            // return std::max(dist_to_max, dist_to_min);  // 外表面固定值
            return dist_to_min;
        }

        return 0.0f;  // 其他区域
    };

    pde.robin = [this, bMin, maxLength](const Vector3& x, const Vector3& n,
                                        bool _) -> float {
        // Vector3 uv = (x - bMin) / maxLength;
        // return this->reflectingBoundaryValue.get(uv)[0];
        return 0.0f;
    };
    pde.robinCoeff = [this](const Vector3& x, const Vector3& n,
                            bool _) -> float { return this->robinCoeff; };
    pde.hasReflectingBoundaryConditions =
        [this, bMin, maxLength](const Vector3& x) -> bool {
        // Vector3 uv = (x - bMin) / maxLength;
        // // return this->isReflectingBoundary.get(uv)[0] > 0;
        // std::cout << "reflecting boundary condition: " << uv << std::endl;
        // bool uv_on_x = (uv[0] < 1e-5) || (uv[0] > 1 - 1e-5);
        // bool uv_on_y = (uv[1] < 1e-5) || (uv[1] > 1 - 1e-5);
        // bool uv_on_z = (uv[2] < 1e-5) || (uv[2] > 1 - 1e-5);
        // if (uv_on_x || uv_on_y || uv_on_z) {
        //     return true;
        // }

        return false;
    };
    pde.areRobinConditionsPureNeumann = robinCoeff == 0.0f;
    pde.areRobinCoeffsNonnegative = robinCoeff >= 0.0f;
    pde.absorptionCoeff = absorptionCoeff;
}

void ModelProblem::partitionBoundaryMesh() {
    // use Zombie's default partitioning function, which assumes the boundary
    // discretization is perfectly adapted to the boundary conditions; this
    // isn't always a correct assumption and the user might want to override
    // this function for their specific problem
    zombie::partitionBoundaryMesh<3>(
        pde.hasReflectingBoundaryConditions, positions, indices,
        absorbingBoundaryPositions, absorbingBoundaryIndices,
        reflectingBoundaryPositions, reflectingBoundaryIndices);
    // std::cout << "partitioned boundary mesh into "
    //           << absorbingBoundaryPositions.size() << "  "
    //           << reflectingBoundaryPositions.size() << "  " << indices.size()
    //           << "  " << positions.size() << "  "
    //           << reflectingBoundaryPositions.size() << "  " << reflectingBoundaryIndices.size() <<  std::endl;
}

void ModelProblem::populateGeometricQueries() {
    // set the domain extent for geometric queries
    queries.domainIsWatertight = domainIsWatertight;
    queries.domainMin = boundingBox.first;
    queries.domainMax = boundingBox.second;

    // use an absorbing boundary handler to populate geometric queries for the
    // absorbing boundary
    absorbingBoundaryHandler.buildAccelerationStructure(
        absorbingBoundaryPositions, absorbingBoundaryIndices);
    zombie::populateGeometricQueriesForDirichletBoundary<3>(
        absorbingBoundaryHandler, queries);

    if (!solveDoubleSided && useSdfForAbsorbingBoundary) {
        // override distance queries to use an SDF grid. The user can also use
        // Zombie to build an SDF hierarchy for double-sided problems (ommited
        // here for simplicity)
        sdfGridForAbsorbingBoundary = std::make_unique<zombie::SdfGrid<3>>(
            queries.domainMin, queries.domainMax);
        zombie::Vector3i sdfGridShape =
            zombie::Vector3i::Constant(sdfGridResolution);
        zombie::populateSdfGrid<3>(absorbingBoundaryHandler,
                                   *sdfGridForAbsorbingBoundary, sdfGridShape);
        zombie::populateGeometricQueriesForDirichletBoundary<zombie::SdfGrid<3>,
                                                             3>(
            *sdfGridForAbsorbingBoundary, queries);
    }

    // use a reflecting boundary handler to populate geometric queries for the
    // reflecting boundary
    std::function<bool(float, int)> ignoreCandidateSilhouette =
        zombie::getIgnoreCandidateSilhouetteCallback(solveDoubleSided);
    std::function<float(float)> branchTraversalWeight =
        zombie::getBranchTraversalWeightCallback();

    if (pde.areRobinConditionsPureNeumann) {
        reflectingNeumannBoundaryHandler.buildAccelerationStructure(
            reflectingBoundaryPositions, reflectingBoundaryIndices,
            ignoreCandidateSilhouette);
        zombie::populateGeometricQueriesForNeumannBoundary<3>(
            reflectingNeumannBoundaryHandler, branchTraversalWeight, queries);

    } else {
        reflectingRobinBoundaryHandler.buildAccelerationStructure(
            reflectingBoundaryPositions, reflectingBoundaryIndices,
            ignoreCandidateSilhouette, minRobinCoeffValues,
            maxRobinCoeffValues);
        zombie::populateGeometricQueriesForRobinBoundary<3>(
            reflectingRobinBoundaryHandler, branchTraversalWeight, queries);
    }
}
