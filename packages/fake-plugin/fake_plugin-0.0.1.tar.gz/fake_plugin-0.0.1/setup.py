from setuptools import setup, find_packages


def get_long_description():
    """
    Remember to updated README.md describing your project.

    It's going to be used on your Pypi page.
    """

    with open("README.md", "r", encoding="UTF-8") as file:
        return file.read()


setup(
    name="fake_plugin",  # your plugin name
    version="0.0.1",  # your plugin version
    install_requires=[],
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: System",
        "Topic :: System :: Hardware",
    ],
    url="https://github.com/quantum-plugins/fake-plugin",
    license="MIT",
    author="Dpbm",
    author_email="dpbm136@gmail.com",
    description="A fake quantum plugin for tests",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
)
