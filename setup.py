from setuptools import find_packages, setup

setup(
    name='dqr',
    packages=find_packages(include = ['src', 'src.*']),
    include_package_data=True,    
    version='0.6.1',
    description='Data Quality Rules for Solvency 2, VNS and FTK',
    author='DeNederlandscheBank',
    license='MIT/X',
    install_requires=[
		'aniso8601',
		'click==7.1.2',
		'cx_Freeze==6.1',
		'data-patterns==0.1.20',
		'dnb-arelle',
		'isodate==0.6.1',
		'Jinja2<3.1.0',
		'jupyter',
		'lxml>=3.4.4',
		'numpy==1.19.5',
		'openpyxl==3.0.5',
		'pandas==1.1.4',
		'python-dotenv>=0.5.1',
		'regex==2018.08.29',
		'requests',
		'Sphinx==1.8.5',
		'sphinx-rtd-theme==0.5.1',
		'tabulate',
		'tox==3.20.0',
		'tqdm',
		'xlrd>=0.9.0',
    ]
)
