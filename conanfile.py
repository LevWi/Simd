from conans import ConanFile, CMake

class SimdConan(ConanFile):
    name = "Simd"
    version = "4.7.102"
    license = "MIT"
    author = "Ermig1979"
    url = "https://github.com/ermig1979/Simd"
    description = "The Simd Library is a free open source image processing and machine learning library, designed for C and C++ programmers"
    topics = ("performance", "optimization", "simd")
    settings = "os", "compiler", "build_type", "arch"
    #options = {"shared": [True, False], "fPIC": [True, False]}
    #default_options = {"shared": False, "fPIC": True}
    generators = "cmake_find_package"
    exports_sources = "src/*", "prj/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="prj/cmake3")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder="prj/cmake3")
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["Simd"]
        # self.cpp_info.set_property("cmake_file_name", "SIMD")
        # self.cpp_info.set_property("cmake_target_name", "SIMD::SIMD")
        # self.cpp_info.set_property("cmake_find_mode", "both")
        # self.cpp_info.libs.append("Simd" if self.settings.os == "Windows" and not self.settings.os.subsystem else "z")

        # self.cpp_info.names["cmake_find_package"] = "SIMD"
        # self.cpp_info.names["cmake_find_package_multi"] = "SIMD"
