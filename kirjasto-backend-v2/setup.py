from setuptools import setup

setup(
    name="kirjasto-backend-v2",
    version="1.0",
    description="",
    keywords="",
    author="",
    packages=["kirjasto-backend-v2"],
    entry_points={"console_scripts": ["kirjasto-backend-v2=kirjasto-backend-v2.main:main"]},
    include_package_data=True,
    zip_safe=False
    )