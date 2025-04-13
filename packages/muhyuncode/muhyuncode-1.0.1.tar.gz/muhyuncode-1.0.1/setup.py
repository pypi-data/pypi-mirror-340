from setuptools import setup

setup(
    name="muhyuncode",
    version="1.0.1",
    description="🐉 무현코드: 한국어 감성 기반 패러디 프로그래밍 언어",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Donghyun Kim",
    author_email="kd.hyun0229@gmail.com",
    url="https://pypi.org/project/muhyuncode/",
    py_modules=["무현코드"],
    entry_points={
        "console_scripts": [
            "muhyun=무현코드:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: Korean",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
