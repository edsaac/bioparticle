from setuptools import setup

setup(
    name='jupypft',
    version='0.1.0',
    description='Handle PFLOTRAN from python',
    url='https://github.com/edsaac/bioparticle',
    author='Edwin Saavedra C.',
    author_email='esaavedrac@u.northwestern.edu',
    license='MIT License',
    packages=['jupypft'],
    install_requires=['numpy',
                      'matplotlib',
                      'ipywidgets'
                      ],

    classifiers=['None'],
)
