from setuptools import setup, find_packages

setup(
    name="aigc_intent_solt",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=2.0.3',
        'flask-cors>=3.0.10',
        'requests>=2.26.0',
        'python-dotenv>=0.19.2',
        'sqlalchemy>=1.4.28'
    ],
    entry_points={
        'console_scripts': [
            'aigc-solt=aigc_intent_solt.app:main'
        ]
    },
    author="Kang Zhao",
    author_email="zhaokanga@h3c.com",
    description="AIGC意图解析解决方案",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="http://117.159.24.209:30381/snappy-expand/aigc-intent-solt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)