
from setuptools import setup, Extension

module = Extension(name='AskCheckSum',sources=['askCheckSum.c'])

setup(name='AskCheckSum',
      version = '1.0.1',
      description = 'AskCheckSum',
      author_email='hufazyj@gmail.com',
      author='hackzy',
      ext_modules = [module],
      package_data={
        '': ['*.pyi'],  # 包含 .pyi 文件
    },
    include_package_data=True,  # 确保包含 package_data 中的文件
      )

'''import setuptools

setuptools.setup(

      name='AskCheckSum',
      version = '1.0.0',
      description = 'askCheckSum',
      author_email='hufazyj@gmail.com',
      author='hackzy',
      packages=setuptools.find_packages(),
      include_package_data=True,

)'''