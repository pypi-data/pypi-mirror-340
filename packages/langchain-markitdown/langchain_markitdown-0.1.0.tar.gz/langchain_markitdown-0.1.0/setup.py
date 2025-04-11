from setuptools import setup, find_packages

setup(
    name='langchain-markitdown',
    version='0.1.0',
    description='LangChain data loaders based on Markdown by @untrueaxioms.',
    author='Nathan Sasto',
    url="https://github.com/nsasto/langchain-markitdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'markitdown[all]',  # Consider specifying a version
        'langchain_core',  # Consider specifying a version
        'langchain-text-splitters',  # Consider specifying a version
        'langchain_openai'  # Consider specifying a version
    ],
    extras_require={
        'dev': [
            'pytest',
            'python-docx',
            'python-pptx',
            'openpyxl',
            'pytest-cov'
            
        ]
    },
    python_requires='>=3.8'  # Specify minimum Python version
)