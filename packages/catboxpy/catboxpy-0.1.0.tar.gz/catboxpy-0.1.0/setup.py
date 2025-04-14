from setuptools import setup, find_packages


setup(
    name='catboxpy',
    version='0.1.0',
    packages=find_packages(),
    description='A Python wrapper for the Catbox.moe api with Async features',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='anshonweb',
    author_email='ansh.a.3112@gmail.com',
    url='https://github.com/anshonweb/catboxpy',
    license='MIT',
    keywords='catbox api python wrapper async',
)