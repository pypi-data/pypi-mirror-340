from setuptools import setup, find_packages

setup(
    name='video_resizer',
    version='0.2',
    description='A Python package to resize videos without losing quality using FFmpeg',
    author='Pratibha',
    packages=find_packages(),
    install_requires=[
        'ffmpeg-python',
    ],
    entry_points={
        'console_scripts': [
            'video_resizer=video_resizer.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
