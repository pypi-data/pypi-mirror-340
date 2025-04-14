from setuptools import setup, find_packages

setup(
    name='aigpt',
    version='0.1',
    description='Python βιβλιοθήκη για επικοινωνία με το OpenAI API μέσω requests',
    author='panoscodergr',
    author_email='panosgiannoulis76@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
