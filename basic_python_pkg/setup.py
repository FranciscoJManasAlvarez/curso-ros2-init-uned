from setuptools import find_packages, setup

package_name = 'basic_python_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Francisco Jose Manas Alvarez',
    maintainer_email='fjmanas@dia.uned.es',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'basic_node = basic_python_pkg.basic_node:main',
            'demo_node = basic_python_pkg.demo_node:main',
            'service_server = basic_python_pkg.service_server:main',
            'service_client = basic_python_pkg.service_client:main',
            'test_topics_services = basic_python_pkg.test_topics_services:main',
            'aux_topics_services = basic_python_pkg.aux_topics_services:main'
        ],
    },
)
