from setuptools import setup, find_packages
                         
setup(
    name="fqxtest",
    version="0.1.9",
    packages=find_packages(),
    description="A python library for Viet Nam stock market data.",
    long_description=open('README.md').read(),
    long_description_content_type = "text/markdown",
    author="FiinLab",
    author_email="fiinlab@fiingroup.vn",
    install_requires=['requests','python-dateutil', 'pandas', 'numpy', 'signalrcore','fastdtw','matplotlib','scipy',
                      'python_dotenv','scikit-learn','plotly','stumpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)