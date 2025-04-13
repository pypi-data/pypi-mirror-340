from setuptools import setup, find_packages
from pathlib import Path

# Get the long description from the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='hey_python',
    version='1.0.3',  # Incrementing version number
    license="MIT",
    author='Ranit Bhowmick',
    author_email='bhowmickranitking@duck.com',
    description='An AI-powered CLI assistant that helps with coding and system tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    url='https://github.com/Kawai-Senpai/hey-python',
    install_requires=[
        'openai>=1.0.0',
        'ultraprint>=3.0.0',
        'python-dotenv>=0.15.0',
        'pydantic>=2.0.0',
        'keyring>=24.0.0',
        'cryptography>=36.0.0',  # Added for fallback encryption
    ],
    entry_points={
        'console_scripts': [
            'hey=hey_cli.hey:main',  # Changed to the new entry point
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
