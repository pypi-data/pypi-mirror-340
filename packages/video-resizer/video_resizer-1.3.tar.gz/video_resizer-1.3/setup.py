from setuptools import setup, find_packages
path = r"D:\packages_\video_resizer\README.md"
with open(path,"r") as f:
    description = f.read()

setup(
    name='video_resizer',
    version='1.3',
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
    long_description=description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
