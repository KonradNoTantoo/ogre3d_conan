from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(option=["ogre3d:with_cg=False"])
    builder.add_common_builds()
    builder.run()

    builder = ConanMultiPackager(option=["ogre3d:with_cg=True"])
    builder.add_common_builds()
    builder.run()
