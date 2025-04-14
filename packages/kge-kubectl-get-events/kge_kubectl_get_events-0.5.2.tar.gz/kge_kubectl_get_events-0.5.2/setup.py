from setuptools import setup, find_packages

setup(
    name="kge-kubectl-get-events",
    version="0.5.2",
    description="Kubernetes utility for viewing pod and failed replicaset events",
    author="Jesse Goodier",
    author_email="31039225+jessegoodier@users.noreply.github.com",
    packages=find_packages(include=['kge']),
    package_data={
        'kge': ['completion/*'],
    },
    install_requires=[
        'kubernetes',
        'colorama',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'kge=kge.cli.main:main',
            'kge-install-completions=kge.completion.install:install_completions',
        ],
    },
    python_requires='>=3.11',
)