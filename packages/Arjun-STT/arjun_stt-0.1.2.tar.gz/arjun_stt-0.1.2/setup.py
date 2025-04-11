from setuptools import setup, find_packages

setup(
    name="Arjun_STT",
    version="0.1.2",
    author="Arjun Manish",
    author_email="arjunmanish1234@gmail.com",
    description="This is a speech-to-text package created by Arjun Manish",
    package_data={
        "Arjun_STT": ["web/*.html", "web/*.css", "web/*.js", "web/*.txt"]
    },
    packages=find_packages(include=['Arjun_STT', 'Arjun_STT.*']),
    install_requires=[  # ✅ corrected spelling from install_requirement
        'selenium',
        'webdriver_manager'
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
