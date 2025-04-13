from setuptools import setup, find_packages

setup(
    name='TotalLog',  # Уникальное имя библиотеки
    version='0.6.dev1',
    packages=find_packages(),  # Автоматически находит пакеты в my_library/
    install_requires=[
        'colorama',
        'pycparser>=2.21',
        'datetime',
    ],
    author='Vanja Nazarenko',
    description='console Loger',
)

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*