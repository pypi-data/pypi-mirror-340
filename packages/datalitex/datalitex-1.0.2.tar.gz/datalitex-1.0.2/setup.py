from setuptools import setup, find_packages

setup(
    name='datalitex',
    version='1.0.2',  # 👈 Bumped version here
    description='Datalitex: Smart Data Assistant for Cleaning, Analyzing & Visualizing CSV and DataFrames',
    author='Vinay Desai',
    author_email='vinay.desai@example.com',  # Optional – replace with your real email
    url='https://github.com/vinaydesai/datalitex',  # Replace with your actual GitHub repo URL
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    keywords='data analysis pandas datalysis cleaning visualization',
    python_requires='>=3.7',
)
