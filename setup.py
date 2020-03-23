import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aws-jupyter',
    version='0.1.18',
    scripts=['aws-jupyter', 'launch-aws-jupyter'] ,
    author="Julaiti Alafate",
    author_email="jalafate@gmail.com",
    description="Launch Jupyter notebook on AWS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arapat/aws-jupyter",
    packages=setuptools.find_packages(),
    install_requires=[
        "awscli",
        "boto",
        "pyyaml",
    ],
    package_data={
        "aws_jupyter": ["scripts/*", "examples/*"],
    },
 )

