from setuptools import setup, find_packages

setup(
    name="cilly",
    version="0.1.3",
    description="A simple programming language interpreter",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        'ply>=3.11',
        'pyreadline3>=3.4.1;platform_system=="Windows"'
    ],
    entry_points={
        'console_scripts': [
            'cilly=cilly.repl:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6"
)