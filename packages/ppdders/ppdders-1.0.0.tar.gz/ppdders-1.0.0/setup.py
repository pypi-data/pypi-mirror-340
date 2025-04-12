from setuptools import setup,find_packages
setup(
    name='ppdders',
    version='1.0.0',
    description='A library management system with user registration, login, and admin functions.',
    author='Your Name',
    author_email='your_email@example.com',
    packages=find_packages(),
    install_requires=[
        # 列出项目依赖的第三方库，如果有
    ],
    entry_points={
        'console_scripts': [
            'library - management - system = library_management_system.main:main',
        ],
    },
)