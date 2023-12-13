from setuptools import setup

with open('requirements.txt', 'r') as f:
    requires = f.read().splitlines()

setup(
    name='patho_grading_gui',
    packages=['patho_grading_gui'],
    version='0.1',
    license='MIT',
    description='Your description here',
    author='sarahrahsl',
    author_email='slschow@uw.edu',
    url='https://github.com/PathoGUI/Patho_grading_GUI.git',
    download_url='https://github.com/PathoGUI/Patho_grading_GUI/archive/main.zip',
    keywords=['Image Analysis', 'GUI', 'Prostate cancer', 'Histology'],
    install_requires=requires,
    python_requires='>=3.6',
)
