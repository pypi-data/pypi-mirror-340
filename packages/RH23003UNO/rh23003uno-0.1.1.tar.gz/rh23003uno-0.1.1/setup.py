from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

with open('README.txt') as f:
    long_description = f.read()
with open('CHANGELOG.txt') as f:
    long_description += '\n\n' + f.read()

setup(
    name='RH23003UNO',
    version='0.1.1',
    description='Este paquete contiene métodos numéricos en Python',
    long_description=long_description,
    long_description_content_type='text/plain',
    author='Isai Hidalgo',
    author_email='isai.arh18@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='métodos numéricos, python',
    packages=find_packages(),
    install_requires=['numpy']
)
