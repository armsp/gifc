from setuptools import setup, find_packages
import sys

if sys.version_info[0] != 3:
    raise RuntimeError('Unsupported python version "{0}"'.format(sys.version_info[0]))

try:
    with open('README.md') as f:
        long_description = f.read()
except:
    long_description = 'This is a nifty little tool written in Python to work with GitHub Gists from command line.'

setup(name='gifc',
      version='0.1',
      description='Github Gists from CLI',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['gist', 'github', 'cli'],
      author='Shantam Raj',
      author_email='shantamdps@gmail.com',
      url='https://github.com/armsp/gifc',
      download_url='',
      include_package_data=True,
      packages=find_packages('gifc'),
      scripts=['gifc'],
      license='GNU GPL v3',
      install_requires=[
          'requests',
          ],
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            ],
      zip_safe=False
      )
