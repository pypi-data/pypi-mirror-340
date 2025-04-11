from setuptools import setup, find_packages

setup(
    name='tpthello',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        #add dependencies here.
        # e.g. 'numpy>=1.11.1
    ],
    # Adding as CLI tool
    entry_points={
        "console_scripts": [
            "tpthello = tpthello:hello",
        ],
    },
)