from setuptools import find_packages, setup

entry_points = {
    'console_scripts': [
        'docx2txt = docx2txt:run'
    ]
}

if __name__ == "__main__":
    setup(
        name='python-docx2txt',
        description='A pure python-based utility to extract text and images from docx files.',
        license='MIT',
        author='Ryan Blakley',
        author_email='rblakley@redhat.com',
        url='https://github.com/ryan-blakley/python-docx2txt',
        version='0.11',
        keywords=['python', 'docx', 'text', 'images', 'extract'],
        packages=find_packages(),
        entry_points=entry_points,
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.11',
        ]
    )
