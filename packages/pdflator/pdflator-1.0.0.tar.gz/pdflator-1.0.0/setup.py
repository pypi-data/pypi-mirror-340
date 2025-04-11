import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdflator",
    version="1.0.0",
    author="Enes Bayram",
    author_email="enes.bayram1@proton.me",
    description="A PDF translator that preserves layout",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bayramenes/PDFlator",
    project_urls={
        "Bug Tracker": "https://github.com/bayramenes/PDFlator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    # package_dir tells setuptools where to find the package source.
    # "": "." means look in the root directory for the package(s) listed in 'packages'.
    package_dir={"": "."},
    # find_packages will now find the 'pdflator' directory in the root.
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.7",
    install_requires=[
        "flask>=3.0.0",
        "pymupdf>=1.22.0", # Consider updating to a more recent version if compatible
        "pymupdf-fonts>=1.0.5",
        "googletrans>=4.0.0", # Note: googletrans can be unstable, consider alternatives if issues persist
        "libretranslatepy>=2.1.4",
        "python-dotenv>=1.0.0",
    ],
    # include_package_data=True tells setuptools to include non-code files
    # specified in MANIFEST.in or found by setuptools itself (like package_data).
    include_package_data=True,
    # package_data explicitly lists data files within the package.
    # This might be slightly redundant with include_package_data=True and MANIFEST.in,
    # but ensures static/templates are included. The path is relative to the package dir.
    package_data={
        "pdflator": [
            "static/**/*",
            "templates/**/*",
        ],
    },
    entry_points={
        "console_scripts": [
            # This should still work as it refers to pdflator (package).main (module):main (function)
            "pdflator=pdflator.main:main",
        ],
    },
)