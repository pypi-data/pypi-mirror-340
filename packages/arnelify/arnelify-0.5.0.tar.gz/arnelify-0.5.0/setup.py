from setuptools import setup, find_packages, Extension

ffi = Extension(
  'arnelify-ffi',
  sources=['arnelify/cpp/ffi.cpp'],
  language='c++',
  extra_compile_args=['-std=c++2b', '-w'],
  include_dirs=['arnelify/cpp/include', '/usr/include', '/usr/include/jsoncpp/json'],
  extra_link_args=['-ljsoncpp', '-lz']
)

setup(
    name="arnelify",
    version="0.5.0",
    author="Arnelify",
    description="Minimalistic dynamic library which is an SDK written in C and C++.",
    url='https://github.com/arnelify/arnelify-python',
    keywords="arnelify arnelify-python arnelify-sdk arnelify-sdk-python",
    packages=find_packages(),
    license="MIT",
    install_requires=["cffi", "setuptools", "wheel"],
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    ext_modules=[ffi],
)