from setuptools import setup, find_packages

setup(
    name="neurovortex",  # Package name
    version="0.1.0",  # Initial version
    author="Boring-Dude",  # Author name
    author_email="cybergx932@gmail.com",  # Author email (add your email here)
    description="An AI Optimizer module for improving performance.",  # Short description
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Long description from README
    long_description_content_type="text/markdown",  # Content type for long description
    url="https://github.com/boring-dude/neurovortex",  # URL to the project repository (update with your repo)
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[
        "torch>=1.9.0",  # Specify minimum versions for dependencies
        "onnx>=1.10.0",
        "tensorflow>=2.6.0",
        "psutil>=5.8.0",
        "gputil>=1.4.0"
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],  # Development dependencies
        "docs": ["sphinx", "sphinx_rtd_theme"],  # Documentation dependencies
    },
    python_requires=">=3.8",  # Specify the minimum Python version
    classifiers=[
        "Development Status :: 3 - Alpha",  # Current development status
        "Intended Audience :: Developers",  # Intended audience
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",  # License type
        "Programming Language :: Python",  # Programming language
        "Programming Language :: Python :: 3",  # Python 3 support
        "Programming Language :: Python :: 3.8",  # Python 3.8 support
        "Programming Language :: Python :: 3.9",  # Python 3.9 support
        "Programming Language :: Python :: 3.10",  # Python 3.10 support
        "Topic :: Scientific/Engineering :: Artificial Intelligence",  # AI-related topic
    ],
    keywords="AI optimization, model optimization, deep learning, performance tuning",  # Keywords for the package
    license="MIT",  # License type
    project_urls={
        "Bug Tracker": "https://github.com/Boring-Dude/neurovortex/issues",  # Bug tracker URL
        "Documentation": "https://github.com/Boring-Dude/neurovortex/wiki",  # Documentation URL
        "Source Code": "https://github.com/Boring-Dude/neurovortex",  # Source code URL
    },
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    zip_safe=False,  # Prevent the package from being installed as a .egg file
)