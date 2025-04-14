
import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent


setup(
    name='SR23002UNO',
    version='1.0.7',
    author='David Enrique Sixco Ramos',
    author_email='sr23002@ues.edu.sv',
    description='Liberia para resolver ecuaciones lineales y no lineales',
    long_description=(HERE / "README.md").read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/sr230002/CDA135-GT02-SR23002UNO',
    license='MIT',
    packages=['SR23002UNO'],
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
)
