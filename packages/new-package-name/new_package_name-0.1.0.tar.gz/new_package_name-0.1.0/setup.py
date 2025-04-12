from setuptools import setup, find_packages

setup(
    name='new_package_name',  # Replace with your package name
    version='0.1.0',   # Update version number
    packages=find_packages(),  # Automatically find the packages in your folder
    install_requires=[],  # Add any dependencies here
    description='A library for financial factors',  # Write a short description
    long_description=open('README.md').read(),  # Read the README file for long description
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/factorlib',  # Update with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Or another license you choose
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
