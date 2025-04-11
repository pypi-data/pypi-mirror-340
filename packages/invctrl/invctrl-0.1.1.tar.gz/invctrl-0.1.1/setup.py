from setuptools import setup, find_packages

setup(
    name="invctrl",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "tinydb",
        "jinja2",
        "asgiref==3.8.1",
        "python-multipart==0.0.20",
        "sqlparse==0.5.0",
        "telnetlib3==2.0.4",
        "tzdata==2024.1",
    ],
    entry_points={
        "console_scripts": [
            "invctrl=invctrl.main:run"
        ]
    },
    author="Indra Setiawan",
    author_email="portgash.the.ace@gmail.com",
    description="A FastAPI-based inventory control system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
