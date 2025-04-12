from setuptools import Require, setup, find_packages

setup(
  name='midoghanam',
  version='0.0.5',
  author='Mohamed Ahmed Ghanam',
  author_email='mghanam883@outlook.com',
  description='مكتبتي الشخصية – midoghanam',
  long_description=open('README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/mido-ghanam',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  install_requires=[
    'requests',
    "re"
  ],
  password="Moh@2009@",
  python_requires='>=3.6',
)
