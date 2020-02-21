from setuptools import setup, find_packages
import vasttools

setup(
    name='treasuremap',
    url='https://github.com/ddobie/TreasureMapPy/',
    author='Dougal Dobie',
    author_email='ddob1600@uni.sydney.edu.au',
    packages=find_packages(),
    version=vasttools.__version__,
    license='MIT',
    description=('Python module to upload pointings to treasuremap.space'),
    install_requires=[],
    scripts=[],
    include_package_data=True
)
