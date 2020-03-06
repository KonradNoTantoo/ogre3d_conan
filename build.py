import build
import os
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    ci_ogre_architecture = os.environ['CI_OGRE_ARCHITECTURE']
    ci_ogre_with_cg = os.environ['CI_OGRE_WITH_CG']

    builder = ConanMultiPackager(docker_32_images=True, pip_install=["mako"])
    builder.add(settings={"arch": ci_ogre_architecture, "build_type": "Release"},
                options={"ogre:with_cg": "ON" == ci_ogre_with_cg})
    builder.add(settings={"arch": ci_ogre_architecture, "build_type": "Debug"},
                options={"ogre:with_cg": "ON" == ci_ogre_with_cg})

    builder.run()
