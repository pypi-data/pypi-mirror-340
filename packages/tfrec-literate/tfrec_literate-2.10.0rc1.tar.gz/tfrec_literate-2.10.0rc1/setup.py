import setuptools

setuptools.setup(
        name="tfrec-literate", # library name will go here
        version="2.10.0rc1", # version info
        author="vwhvpwvk",
        description="Library for reading and writing TFRecords",
        url="https://github.com/vwhvpwvk/tfrec-literate",
        packages=setuptools.find_packages(),
        install_requires=[
            'tensorflow<2.13'#,
		#'opencv-python-headless',
		#'tqdm'
            ],
      project_urls={
                "Source Code": "https://github.com/vwhvpwvk/tfrec-literate"
            }
)

