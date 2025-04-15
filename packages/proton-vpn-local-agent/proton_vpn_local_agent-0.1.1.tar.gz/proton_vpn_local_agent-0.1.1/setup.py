#!/usr/bin/env python

from setuptools import setup


setup(
    name="proton-vpn-local-agent",
    version="0.1.1",
    description="Local agent library",
    author="Proton AG",
    author_email="opensource@proton.me",
    url="https://github.com/ProtonVPN/local-agent-rs",
    include_package_data=False,
    python_requires=">=3.9",
    license="GPLv3",
    platforms="Linux",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Security",
    ],
)
