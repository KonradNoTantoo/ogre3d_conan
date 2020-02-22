from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(options=["ogre3d:with_cg=False"], docker_32_images=True, pip_install=["mako"])
    builder.add_common_builds()
    builder.run()

    builder = ConanMultiPackager(options=["ogre3d:with_cg=True"], docker_32_images=True, pip_install=["mako"])
    builder.add_common_builds()
    builder.run()
