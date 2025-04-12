from setuptools import setup, find_packages

setup(
    name="langchain-datura",  # Replace with your desired package name
    version="0.1.0",  # Initial version
    author="Datura",  # Replace with your name
    author_email="your-email@example.com",  # Replace with your email
    description="LangChain integration with Datura API for search and data-fetching tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Datura-ai/langchain-datura",  # Replace with your GitHub repo URL
    packages=find_packages(),
    include_package_data=True,
       install_requires=[
        "langchain-core==0.3.51",
        "langchain==0.3.23", 
        "pydantic==2.11.3",
        "python-dotenv==1.1.0",
        "datura-py==0.0.15",
        "pytest==8.3.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
