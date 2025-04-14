from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='automatix_cmd',
    version='2.5.99',
    description='Automation wrapper for bash and python commands',
    keywords=['bash', 'shell', 'command', 'automation', 'process', 'wrapper', 'devops', 'system administration'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vanadinit/automatix_cmd',
    author='Johannes Paul',
    author_email='vanadinit@quantentunnel.de',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'automatix=automatix:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
