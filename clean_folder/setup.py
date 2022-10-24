from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.1b',
    description='Script sort target folder',
    url='https://github.com/xoka-pro/goit-python-core-HW06',
    author='Oleh Ovchinnikov',
    author_email='xokzzz@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:general']}
)