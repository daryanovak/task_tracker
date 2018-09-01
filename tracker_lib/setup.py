from setuptools import setup, find_packages

setup(
    name='tracker_lib',
    version="3.0",
    license='MIT',
    description='tracker library',
    author='Darya Novak',
    author_email='darya_novak@gmail.com',
    packages=find_packages(),
    include_package_data=False,
    install_requires=["croniter", "pony","psycopg2"],
)