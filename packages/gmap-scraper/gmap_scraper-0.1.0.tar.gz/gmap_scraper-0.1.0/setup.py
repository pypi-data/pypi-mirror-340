from setuptools import setup, find_packages

setup(
    name='gmap_scraper',
    version='0.1.0',
    description='Scrape business data from Google Maps using Selenium and Streamlit',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/mukhtar-ul-islam88/Leads_generation_gmap_business',
    packages=find_packages(),
    install_requires=[
        'selenium-wire',
        'streamlit',
        'webdriver-manager',
    ],
    entry_points={
        'console_scripts': [
            'gmap-scraper=streamlit_app:main',  # Optional CLI entrypoint
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
