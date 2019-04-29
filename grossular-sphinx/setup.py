
from setuptools import  find_packages,setup
setup(
    name='grossularsphinx',
    version='0.0dev',
    packages=find_packages,
    url='https://github.com/CNLHC/grossular/',
    author='HanCheng Liu',
    author_email='cn_lhc@qq.com',
    description='grossular sphinx extension',
    platforms='any',
    license='MIT',
    long_description=open('README.txt').read(),
    namespace_packages=['grossularsphinx'],
)