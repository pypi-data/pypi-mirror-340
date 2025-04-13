from setuptools import setup, find_packages

setup(
    name="simple-streamlit-calculator",
    version="1.0.0",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0"
    ],
    entry_points={
        "console_scripts": [
            "calculator=calculator_app.calculator_app:main"
        ]
    },
    python_requires='>=3.7',
)
