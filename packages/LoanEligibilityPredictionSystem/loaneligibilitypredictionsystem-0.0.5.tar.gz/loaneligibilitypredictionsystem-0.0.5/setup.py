from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='LoanEligibilityPredictionSystem',
    version='0.0.5',
    description='Basic loan eligibilty predictor',
    long_description=open('README.md', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # 🔥 This line fixes the PyPI error
    url='',
    author='Ahriel, Gyanu, Jamie, Sulav, Will',
    author_email='ayoung08@rams.shepherd.edu, gbasne01@rams.shepherd.edu, jkemma01@rams.shepherd.edu, sbista01@rams.shepherd.edu, wneigh01@rams.shelherd.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='loan, predictor, eligibilty',
    packages=find_packages(),
    install_requires=['pandas']
)