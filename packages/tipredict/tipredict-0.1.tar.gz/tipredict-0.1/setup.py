from setuptools import setup, find_packages

setup(name='tipredict',
      version='0.1',
      packages=find_packages(),
      include_package_data=True,
      package_data={
        "tipredict": ["*.csv","weights/*.pth"]
    },
      install_requires=[
          'numpy>=1.24.3',
          'pandas>=1.3.4',
          'tqdm>=4.66.4'
      ])
