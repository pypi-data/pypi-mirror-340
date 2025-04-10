from setuptools import setup, find_packages

setup(
    name='Menataur',
    version='1.0',
    packages=find_packages(),
    license='MIT',
    author='Gratonic',
    author_email='Gratonic@proton.me',
    description='Menu Interface Builder for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Gratonic/Menataur',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Any',
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[
        'colorama',  # Specify colorama as a dependency
    ],
)