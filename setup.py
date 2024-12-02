from setuptools import setup, find_packages

setup(
    name='com-port-selection-tool',
    version='1.0.0',
    description='A PyQt6-based COM port selection tool',
    long_description=open('README.md', encoding='utf-8').read(),  # Укажите кодировку
    long_description_content_type='text/markdown',
    author='Molisc',
    author_email='ivanrudko445@gmail.com',
    packages=find_packages(),  # Поиск всех пакетов (например, comsel, comsel.icons)
    include_package_data=True,  # Включение данных из MANIFEST.in
    install_requires=[
        'PyQt6',
        'pyserial',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)