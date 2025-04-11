from setuptools import setup, find_packages

setup(
    name='ai_agent_app',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
        # Example: 'numpy>=1.18.0',
    ],
    author='Sebastian Coros',
    author_email='sebastian.coros@dell.com',
    description='ai agent CIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sebastian_coros/ai_agent_app',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)