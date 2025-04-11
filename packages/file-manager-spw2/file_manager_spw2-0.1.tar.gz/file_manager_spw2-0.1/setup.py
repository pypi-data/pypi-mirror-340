from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='file_manager_spw2',
    packages=['file_manager_spw2'],  # this must be the same as the name above
    version='0.1',
    description='un tipo de gestor de archivos',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='spw2',
    author_email='mr.reich.oficial.1@gmail.com',
    # use the URL to the github repo
    url='https://github.com/Mrreich/file_manager_reichtangle',
    download_url='https://github.com/Mrreich/file_manager_reichtangle/releases/tag/v0.1',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)