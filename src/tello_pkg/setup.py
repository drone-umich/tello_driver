from setuptools import setup

package_name = 'tello_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='albertocastro',
    maintainer_email='josealberto.castro@udem.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "controller_node = tello_pkg.controller_node:main",
            "receiver_node = tello_pkg.receiver_node:main",
            "cam_node = tello_pkg.cam_receiver_node:main"
        ],
    },
)
