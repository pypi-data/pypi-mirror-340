from setuptools import setup, find_packages

setup(
    name='rakuten_recipe_scraping',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    author='gesouni',
    author_email='w5eq4hgv7q6y@gmail.com',
    description='楽天レシピのデータをスクレイピングするためのライブラリ',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gesouni/rakuten_recipe_scraping',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
