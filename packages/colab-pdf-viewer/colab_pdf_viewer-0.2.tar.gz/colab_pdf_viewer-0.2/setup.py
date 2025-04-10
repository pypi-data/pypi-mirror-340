from setuptools import setup, find_packages

setup(
    name='colab_pdf_viewer',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pdf2image',
        'ipython',
    ],
    description='A simple tool to display scrollable PDFs in Colab or Jupyter Notebook.',
    author='Marc86316',
    author_email='your_email@example.com',
    url='https://github.com/Marc86316/colab_pdf_viewer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
