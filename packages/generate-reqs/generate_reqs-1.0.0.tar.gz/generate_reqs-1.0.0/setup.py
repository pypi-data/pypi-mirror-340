try:
    from setuptools import setup, find_packages
except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
    from setuptools import setup, find_packages

setup(
    name='generate-reqs',
    version='1.0.0',
    description='Generate requirements.txt with latest stable versions from a YAML file.',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
        'packaging',
    ],
    entry_points={
        'console_scripts': [
            'generate-reqs=generate_reqs.cli:main',
        ],
    },
    python_requires='>=3.7',
)
