from setuptools import setup, find_packages

from setuptools import setup, find_packages

setup(
    name='logia',  # Required: The package name
    version='0.0.1',  # Required: Initial version
    packages=find_packages(),  # Required: Automatically discovers packages in your project
    install_requires=[],  # Optional: Add dependencies here if you need any
    author='',  # Optional: Leave blank for now
    author_email='',  # Optional: Leave blank for now
    description='Simply printing Hello from Logia :)',  # Optional: A brief description
    long_description='',  # Optional: Leave blank for now, could add README content later
    long_description_content_type='text/markdown',  # Optional: Optional, but recommended if using markdown
    url='',  # Optional: Your project's URL (e.g., GitHub repo URL)
    classifiers=[  # Optional: Add classifiers if needed
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',  # Optional: Specify Python version requirement
)
