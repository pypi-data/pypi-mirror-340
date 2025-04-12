from setuptools import setup, find_packages

setup(
	name='questra',
	version='0.4',
	packages=find_packages(),
	install_requires=["cloudscraper", "httpx", "bs4", "fake-useragent"],
	author='Siri_Lv',
	description='Search is a powerful library for convenient searching.',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'],
        python_requires='>=3.8',
        keywords=[
            "search",
            "google",
            "bing",
            "translation",
            "image-search",
            "image"
        ],
)
