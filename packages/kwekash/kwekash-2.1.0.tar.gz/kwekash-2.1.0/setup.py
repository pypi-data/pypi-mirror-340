from setuptools import setup

setup(
    name="kwekash",
    version="2.1.0",
    description="Run weka commands in WEKA drive pods inside Kubernetes.",
    author="Rodney Peck",
    author_email="fogcat5@gmail.com",
    license="MIT",
    packages=["kwekash"],
    entry_points={
        "console_scripts": [
            "kwekash = kwekash.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)
