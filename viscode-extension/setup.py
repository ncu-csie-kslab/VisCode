import setuptools

setuptools.setup(
    name="viscode-extension",
    version='0.0.6',
    url="",
    author="jhliao",
    author_email="",
    license="BSD 3-Clause",
    description="Jupyter server viscode extension",
    packages=setuptools.find_packages(),
    # package_dir={'mypluging':'mypluging'},
    include_package_data=True,
    package_data={
        'viscode': [
            'nbextension/*/*.js',
            'nbextension/*/*.css',
            'nbextension/*/*.html',
        ]
    },
    install_requires=['tornado', 'notebook'],
    classifiers=[
        'Framework :: Jupyter',
    ]
)
