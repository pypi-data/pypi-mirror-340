
from setuptools import setup, find_packages

setup(
    name="orange-earthdata_mcp_server",
    version="None",
    description="None",
    author="orange",
    author_email="support@orange.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['earthaccess', 'mcp[cli]>=1.2.1', 'rich'],
    keywords=["orange"] + ['Earthdata'],
)
