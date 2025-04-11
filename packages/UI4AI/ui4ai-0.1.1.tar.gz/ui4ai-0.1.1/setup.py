from setuptools import setup, find_packages

setup(
    name="UI4AI",
    version="0.1.1",
    author="Kethan Dosapati",
    description="Streamlit UI for LLM chat apps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["streamlit"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
