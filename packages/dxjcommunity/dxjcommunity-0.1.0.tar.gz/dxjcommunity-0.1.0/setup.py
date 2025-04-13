from setuptools import setup, find_packages

setup(
    name='dxjcommunity',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,  # Pastikan file asset (jika ada) ikut disertakan
    description='Modul DROPXJUNGLER untuk menampilkan logo ASCII dan fungsi pendukung lainnya',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='dxjcommunity',
    author_email='frendicahyow@gmail.com',
    url='https://github.com/ntfound-dev/modul001',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
