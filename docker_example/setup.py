from setuptools import setup, find_packages

setup(
    name='docker_example',
    version='1.0.0',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['pandas', 'flask', 'Flask-HTTPAuth', 'gunicorn', 'requests'],
    entry_points={
        "console_scripts": [
            "download=docker_example.download_ratings.download_ratings:main",
            "get=docker_example.get_ratings.get_ratings:main",
            "rank=docker_example.rank_ratings.rank_ratings:main"
        ]
    }
)
