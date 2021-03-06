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
        "bites": [True, False],
        "direct3d9_renderer": [True, False],
        "direct3d11_renderer": [True, False],
        "opengl_renderer": [True, False],
        "opengl3_renderer": [True, False],
        "opengles_renderer": [True, False],
        }

    default_options = {
        "with_cg": False,
        "with_boost": True,
        "with_poco": False,
        "samples": False,
        "with_python": False,
        "with_csharp": False,
        "with_java": False,
        "bites": False,
        "direct3d9_renderer": False,
        "direct3d11_renderer": False,
        "opengl_renderer": False,
        "opengl3_renderer": False,
        "opengles_renderer": False,
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


    def configure(self):
        # we only need sdl for IO control
        self.options["sdl2"].fPIC = False
        self.options["sdl2"].iconv = False
        self.options["sdl2"].sdl2main = False

        if self.settings.os == "Linux":
            self.options["sdl2"].alsa = False
            self.options["sdl2"].jack = False
            self.options["sdl2"].pulse = False
            self.options["sdl2"].nas = False
            self.options["sdl2"].xcursor = False
            self.options["sdl2"].xinerama = False
            self.options["sdl2"].xinput = False
            self.options["sdl2"].xrandr = False
            self.options["sdl2"].xscrnsaver = False
            self.options["sdl2"].xshape = False
            self.options["sdl2"].xvm = False

        if self.settings.os != "Windows":
            del self.options.direct3d9_renderer
            del self.options.direct3d11_renderer


    def requirements(self):
        if self.options.with_boost:
            self.requires("boost/1.71.0@conan/stable")

        if self.options.with_poco:
            self.requires("poco/1.9.4")

        if self.options.with_cg:
            self.requires("nvidia-cg-toolkit-binaries/3.1.0013@utopia/testing")

        if self.settings.os == "Linux" and self.options.bites:
            self.requires("libxaw/1.0.13@bincrafters/stable")


    def source(self):
        tools.replace_in_file("{}/CMakeLists.txt".format(self.folder_name), "project(OGRE VERSION 1.12.5)",
                              '''project(OGRE VERSION 1.12.5)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
link_libraries(${CONAN_LIBS})
add_compile_definitions(GLEW_NO_GLU)''')


    def configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["OGRE_BUILD_DEPENDENCIES"] = "NO" # use libraries built by conan

        cmake.definitions["OGRE_COPY_DEPENDENCIES"] = "OFF"
        cmake.definitions["OGRE_INSTALL_DEPENDENCIES"] = "OFF"
        cmake.definitions["OGRE_INSTALL_PDB"] = "ON"
        cmake.definitions["OGRE_BUILD_PLUGIN_CG"] = "ON" if self.options.with_cg else "OFF"
        cmake.definitions["OGRE_BUILD_SAMPLES"] = "ON" if self.options.samples else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_PYTHON"] = "ON" if self.options.with_python else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_CSHARP"] = "ON" if self.options.with_csharp else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_JAVA"] = "ON" if self.options.with_java else "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_BITES"] = "ON" if self.options.bites else "OFF"

        if self.settings.os == "Windows":
            cmake.definitions["OGRE_BUILD_RENDERSYSTEM_D3D9"] = "ON" if self.options.direct3d9_renderer else "OFF"
            cmake.definitions["OGRE_BUILD_RENDERSYSTEM_D3D11"] = "ON" if self.options.direct3d11_renderer else "OFF"

        cmake.definitions["OGRE_BUILD_RENDERSYSTEM_GL3PLUS"] = "ON" if self.options.opengl_renderer else "OFF"
        cmake.definitions["OGRE_BUILD_RENDERSYSTEM_GL"] = "ON" if self.options.opengl3_renderer else "OFF"
        cmake.definitions["OGRE_BUILD_RENDERSYSTEM_GLES2"] = "ON" if self.options.opengles_renderer else "OFF"

        cmake.configure(source_folder=self.folder_name)
        return cmake


    def build(self):
        cmake = self.configure_cmake()
        cmake.build()


    def package(self):
        cmake = self.configure_cmake()
        cmake.install()


    def package_info(self):
        libs = [
            "OgreMain",
            "OgreOverlay",
            "OgrePaging",
            "OgreProperty",
            "OgreRTShaderSystem",
            "OgreTerrain",
            "OgreVolume",
        ]

        if self.options.bites: libs.append("OgreBites")

        self.cpp_info.includedirs.append("include/OGRE")

        if self.settings.compiler == "Visual Studio" and self.settings.build_type == "Debug":
            self.cpp_info.libs = [lib + "_d" for lib in libs]
        else:
            self.cpp_info.libs = libs
