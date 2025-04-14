import setuptools
from src.bubot import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bubot_core',
    version=__version__,
    author="Razgovorov Mikhail",
    author_email="1338833@gmail.com",
    description="iot framework based on OCF specification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/businka/Bubot_Core",
    package_dir={'': 'src'},
    package_data={
        '': ['*.md', '*.json'],
    },
    packages=setuptools.find_namespace_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    python_requires='>=3.8',
    zip_safe=False,
    install_requires=[
        'cbor2>5',
        'Bubot_Helpers>=4.0.3',
        'Bubot_CoAP>=2.0.0',
    ],
    entry_points={
        'console_scripts':
            [
                'bubot = Bubot.Core:main',
                'Bubot = Bubot.Core:main'
            ]
    }
)
