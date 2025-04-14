#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "mlc::mlc-static" for configuration "RelWithDebInfo"
set_property(TARGET mlc::mlc-static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(mlc::mlc-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELWITHDEBINFO "CXX"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/mlc/libmlc-static.a"
  )

list(APPEND _cmake_import_check_targets mlc::mlc-static )
list(APPEND _cmake_import_check_files_for_mlc::mlc-static "${_IMPORT_PREFIX}/lib/mlc/libmlc-static.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
