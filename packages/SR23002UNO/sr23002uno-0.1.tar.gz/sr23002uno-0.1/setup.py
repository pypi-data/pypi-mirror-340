
import pathlib
from setuptools import setup, find_packages
HERE = pathlib.Path(__file__).parent


setup(
    name='SR23002UNO',
    version='0.1',
    author='David Enrique Sixco Ramos',
    author_email='sr23002@ues.edu.sv',
    description='Liberia para resolver ecuaciones',
    long_description=(HERE / "README.md").read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/davidsixco/CDA135-GT02-SR23002UNO',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
