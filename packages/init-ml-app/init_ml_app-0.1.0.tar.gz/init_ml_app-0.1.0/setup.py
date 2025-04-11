from setuptools import setup, find_packages

setup(
    name='init-ml-app', # The name users will use to install (pip install init-ml-app)
    version='0.1.0',
    packages=find_packages(), # Or specify manually: packages=['your_package_name']
    include_package_data=True, # If you have non-code files in MANIFEST.in
    install_requires=[
        'click>=7.0', # Specify dependencies
    ],
    entry_points={
        'console_scripts': [
            'init-ml-app = ml_project_initializer.cli:main', # Command name = module:function
        ],
    },
    # Metadata
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool to initialize ML and AI project structures.',
#    long_description=open('README.md').read(), # Optional: Use a README for description
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/init-ml-app', # Optional: Project URL
    classifiers=[ # Optional: PyPI classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Choose a license
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.7', # Specify compatible Python versions
)