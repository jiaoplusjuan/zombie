cmake_minimum_required(VERSION 3.15...3.27)
project(zombie-demo_3d)

set(ZOMBIE_DEMO_SRC_FILES
    "config.h"
    "colormap.h"
    "image.h"
    "model_problem.h"
    "grid.h"
)

# add dependencies
list(APPEND ZOMBIE_DEMO_DEPS_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/deps/stb)
list(APPEND ZOMBIE_DEMO_DEPS_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/deps/nlohmann)

# build demo
add_executable(demo_3d demo_3d.cpp ${ZOMBIE_DEMO_SRC_FILES})
target_include_directories(demo_3d PRIVATE ${ZOMBIE_DEMO_DEPS_INCLUDES})
target_link_libraries(demo_3d zombie)

if(MSVC)
    target_compile_options(demo_3d PRIVATE /bigobj)
endif()

message(STATUS "FCPW_SLANG_LIBRARY = ${FCPW_SLANG_LIBRARY}")
message(STATUS "FCPW_SLANG_GLSLANG_LIBRARY = ${FCPW_SLANG_GLSLANG_LIBRARY}")
message(STATUS "FCPW_GFX_LIBRARY = ${FCPW_GFX_LIBRARY}")
message(STATUS "FCPW_SLANG_INCLUDES = ${FCPW_SLANG_INCLUDES}")


if (FCPW_ENABLE_GPU_SUPPORT)
    # target_link_libraries(demo ${FCPW_SLANG_LIBRARY})
    # target_link_libraries(demo ${FCPW_SLANG_GLSLANG_LIBRARY})
    # target_link_libraries(demo ${FCPW_GFX_LIBRARY})
    # target_link_libraries(demo
    #     ${FCPW_SLANG_LIBRARY}
    #     ${FCPW_SLANG_GLSLANG_LIBRARY}
    #     ${FCPW_GFX_LIBRARY}
    # )
    message("USE GPU SUPPORT")
    target_compile_definitions(demo PRIVATE -DFCPW_USE_GPU_LUYAN)
    target_link_libraries(demo
    ${FCPW_GFX_LIBRARY}
    ${FCPW_SLANG_LIBRARY}
    ${FCPW_SLANG_GLSLANG_LIBRARY}
    ${FCPW_SLANG_RT_LIBRARY}
    )
    target_include_directories(demo PRIVATE ${FCPW_SLANG_INCLUDES})
    # target_link_libraries(demo "/usr/lib/x86_64-linux-gnu/libslang.so")
    # target_link_libraries(demo "/usr/local/lib/libslang-glslang.so")
    # target_link_libraries(demo "/usr/local/lib/libgfx.so")
    # target_include_directories(demo PRIVATE ${FCPW_SLANG_INCLUDES})
endif()