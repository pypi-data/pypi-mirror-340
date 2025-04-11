from setuptools import setup,find_packages

setup(
    name='Kani-STT',
    version='0.1',
    author='Kanishk Yadav',
    author_email='pavikani69@gmail.com',
    description='this is speech to text package created by kanishk yadav'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]
