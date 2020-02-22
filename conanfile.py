from conans import ConanFile, CMake, tools
import os


class Ogre3dConan(ConanFile):
    name = "ogre3d"
    version = "1.12.5"
    license = "MIT"
    author = "konrad"
    url = "https://github.com/KonradNoTantoo/ogre3d_conan"
    description = "3D graphics rendering engine"
    topics = ("graphics", "3D rendering", "3D", "conan")
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "with_cg": [True, False],
        "with_boost": [True, False],
        "with_poco": [True, False],
        "samples": [True, False],
        "with_python": [True, False],
        "with_csharp": [True, False],
        "with_java": [True, False],
        }

    default_options = {
        "with_cg": False,
        "with_boost": True,
        "with_poco": False,
        "samples": False,
        "with_python": False,
        "with_csharp": False,
        "with_java": False,
        }

    generators = "cmake"

    requires = [
        ("bzip2/1.0.8@conan/stable", "override"),
        ("libpng/1.6.37@bincrafters/stable", "override"),
        ("freetype/2.10.0@bincrafters/stable"),
        ("zlib/1.2.11@conan/stable"),
        ("pugixml/1.10@bincrafters/stable"),
        ("sdl2/2.0.10@bincrafters/stable"),
        ("zziplib/0.13.69@utopia/testing"),
        # ("ois/1.5@utopia/testing"), # for older versions
        ("freeimage/3.18.0@utopia/testing"),
    ]

    folder_name = "ogre-{}".format(version)

    # using scm is a workaround for https://github.com/OGRECave/ogre/issues/1332
    scm = {
        "type": "git",
        "subfolder": folder_name,
        "url": "https://github.com/OGRECave/ogre.git",
        "revision": "v{}".format(version),
        "submodule": "recursive" 
    }


    def requirements(self):
        if self.options.with_boost:
            self.requires("boost/1.71.0@conan/stable")

        if self.options.with_poco:
            self.requires("poco/1.9.4")

        if self.options.with_cg:
            self.requires("nvidia-cg-toolkit-binaries/3.1.0013@utopia/testing")


    def source(self):
        tools.replace_in_file("{}/CMakeLists.txt".format(self.folder_name), "project(OGRE VERSION 1.12.5)",
                              '''project(OGRE VERSION 1.12.5)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
link_libraries(${CONAN_LIBS})''')


    def configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["OGRE_BUILD_DEPENDENCIES"]="NO" # use libraries built by conan

        cmake.definitions["OGRE_COPY_DEPENDENCIES"] = "OFF"
        cmake.definitions["OGRE_INSTALL_DEPENDENCIES"] = "OFF"
        cmake.definitions["OGRE_INSTALL_PDB"] = "ON"
        cmake.definitions["OGRE_BUILD_PLUGIN_CG"] = "ON" if self.options.with_cg else "OFF"
        cmake.definitions["OGRE_BUILD_SAMPLES"] = "ON" if self.options.samples else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_PYTHON"] = "ON" if self.options.with_python else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_CSHARP"] = "ON" if self.options.with_csharp else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_JAVA"] = "ON" if self.options.with_java else "OFF"

        cmake.configure(source_folder=self.folder_name)
        return cmake


    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()


    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "OGRE")]

        libs = [
            "OgreBites"
            "OgreMain",
            "OgreOverlay",
            "OgrePaging",
            "OgreProperty",
            "OgreRTShaderSystem",
            "OgreTerrain",
            "OgreVolume",
        ]

        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = [lib + "_d" if self.settings.build_type == "Debug" else lib for lib in libs]
            folder = "Debug" if self.settings.build_type == "Debug" else "Release"
            self.cpp_info.libdirs = [os.path.join("lib", folder)]
            self.cpp_info.bindirs = [os.path.join("bin", folder)]
        else:
            self.cpp_info.libs = [
                "lib{}_d.so".format(lib) if self.settings.build_type == "Debug" else "lib{}.so".format(lib)  for lib in libs
            ]

