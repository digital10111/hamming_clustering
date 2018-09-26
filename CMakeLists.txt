cmake_minimum_required( VERSION 3.3 )

project( BoostPythonHelloWorld )

set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")


# Find necessary packages
find_package( PythonLibs 2.7 REQUIRED )
include_directories( ${PYTHON_INCLUDE_DIRS} )

find_package( Boost COMPONENTS python REQUIRED )
include_directories( ${Boost_INCLUDE_DIR} )

# Build our library
#add_library( greet SHARED greet.cpp )

# Define the wrapper library that wraps our library
add_library( unionfind SHARED unionfind.cpp )
target_link_libraries( unionfind ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )
# don't prepend wrapper library name with lib
set_target_properties( unionfind PROPERTIES PREFIX "" )