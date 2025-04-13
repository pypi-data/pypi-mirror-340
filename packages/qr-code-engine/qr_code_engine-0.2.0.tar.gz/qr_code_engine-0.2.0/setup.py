from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='qr_code_engine',  # Replace with your package name
    version='0.2.0',  # Set your version number
    packages=find_packages(),  # This will find all the packages in your project
    install_requires=[
        'qrcode==8.0',  # Specify a valid version
        'Pillow==10.4.0',  # Specify a valid version
        'customtkinter==5.2.2',  # Specify the version if necessary (check for correct version)
		#'customtkinter @ git+https://github.com/TomSchimansky/CustomTkinter.git',
		'packaging'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Set the description type to markdown
    author='Kuldeep Singh aka Aby',
    author_email='shergillkuldeep@outlook.com',
    description='This program helps to generate QR codes with a user interface',
    license='MIT',  # Choose the license that applies
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version requirement
    
    entry_points={  # Add this part to define your command-line interface
        'console_scripts': [
            'qr-gen=qr_code_engine.mainwindow:run_app',  # Entry point to run the GUI
        ],
    },
)
