from setuptools import setup, find_packages

setup(
    name='nkrean',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'play-video = video_player.player:play_video'
        ]
    },
)
