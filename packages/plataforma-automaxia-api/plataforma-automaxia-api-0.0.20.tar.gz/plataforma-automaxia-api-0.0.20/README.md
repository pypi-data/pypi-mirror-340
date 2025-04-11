# Material de apoio

O primeiro passo é ter o código de sua biblioteca separado em uma pasta

  

*   meu\_pacote/ # Pasta do projeto
    *   codigos\_da\_biblioteca/ # Diretório onde deve ficar os códigos de sua biblioteca
    *   LICENCE # Um arquivo com a licença da sua lib
    *   [README.MD](http://README.MD) # Uma descrição do projeto
    *   [setup.py](http://setup.py) # Código Python responsável pelo empacotamento

  

Adicione uma licença

```plain
The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

  

Adicione um readme

```markdown
# Sua descrição aqui
```

  

Instale a lib setuptools

```plain
pip install setuptools
```

  

Crie o [setup.py](http://setup.py)

```plain
from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='wrapper-panda-video',
    version='0.0.1',
    license='MIT License',
    author='Caio Sampaio',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='caio@pythonando.com.br',
    keywords='panda video',
    description=u'Wrapper não oficial do Panda Video',
    packages=['panda_video'],
    install_requires=['requests'],)
```

  

Execute o comando

```plain
python setup.py sdist
```

  

Instale o twine para fazer o upload para o pypi

```plain
pip install twine
```

  

Crie uma conta no pypi

  

Execute o comando para criar um repositório de teste

```plain
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

  

Ou para criar um repositório oficial:

```plain
python setup.py sdist
twine upload dist/*
user: __token__
pass: pypi-AgEIcHlwaS5vcmcCJDZjODVkOTQxLTdmYTQtNDlkZC04NjU3LTZlNWJkZmRhMTU4MgACIFsxLFsicGxhdGFmb3JtYS1hdXRvbWF4aWEtYXBpIl1dAAIsWzIsWyI3ODRkZmYyMC0xNDZhLTQ2NTUtOTc5NS1lY2VjMWQ0NzdlMzciXV0AAAYgSn2xPiG2sMVnN1h50YP1HcJWEgebYttaczKVTijXCxQ


twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDFlN2NlM2ExLTdhZWQtNGZmMC1hYzk5LTExYjEwZDBkY2I4OAACIFsxLFsicGxhdGFmb3JtYS1hdXRvbWF4aWEtYXBpIl1dAAIsWzIsWyI3ODRkZmYyMC0xNDZhLTQ2NTUtOTc5NS1lY2VjMWQ0NzdlMzciXV0AAAYgsLhvhtz5adT7lJXulDhRYtL3duM5yiOTImlWqT0tBF8 dist/*
```
pypi-AgEIcHlwaS5vcmcCJDdkMTI4NjY5LWM5YmEtNDJiOC04OGNkLTFkMmRmOWEzNzE3NAACKlszLCI0OWI3YTc0OS03NDViLTQ2ZTAtYjkzZS05OTAxZGZhMGI2ZTIiXQAABiAAEL1XGUJwrn_9_-rTAtFiTogKFdOfDMpqb649_YCerw