# AC12066UNO

**AC12066UNO** es una librería en Python para resolver sistemas de ecuaciones lineales y no lineales usando varios métodos matemáticos, como Gauss, Gauss-Jordan, Cramer, LU, Jacobi, Gauss-Seidel y Bisección.

## Instalación

Puedes instalar la librería desde PyPI usando pip:

```bash
pip install AC12066UNO


#### 1.2 **Comentarios en el código:**
Asegúrate de que todas las funciones estén bien documentadas usando **docstrings**. Esto facilita tanto el uso como el mantenimiento de la librería. Ya lo estás haciendo muy bien en tu código, solo verifica que no falte ningún detalle importante.

### 🌐 **2. Subir la librería a PyPI:**

#### 2.1 **Crear un archivo `setup.py`:**
Este archivo contiene toda la información sobre tu librería para PyPI, incluyendo nombre, versión, autor, dependencias y demás. Aquí tienes un ejemplo básico:

```python
from setuptools import setup, find_packages

setup(
    name='AC12066UNO',
    version='0.1.0',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Martín',
    author_email='martin.a.ac@outlook.com',
    url='https://github.com/ale-0293/AC12066UNO',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
