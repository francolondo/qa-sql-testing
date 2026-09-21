# QA Database Testing — SQLite

![DB Tests](https://github.com/francolondo/qa-sql-testing/actions/workflows/tests.yml/badge.svg)

Proyecto de práctica enfocado en pruebas de integridad de base de datos: validación de restricciones de esquema (claves únicas, claves foráneas, checks) y reglas de negocio sobre los datos, usando SQLite y pytest.

## Qué incluye este repositorio

| Archivo | Descripción |
|---|---|
| `schema.sql` | Esquema de una base de datos de e-commerce simplificada (usuarios, productos, pedidos, items) con restricciones de integridad |
| `casos_de_prueba_sql.md` | Plan de pruebas manual con 10 casos, cubriendo restricciones de esquema y reglas de negocio |
| `test_database.py` | Automatización de esos 10 casos con pytest sobre una base de datos SQLite en memoria |
| `requirements.txt` | Dependencias de Python del proyecto |
| `.github/workflows/tests.yml` | Workflow de GitHub Actions que ejecuta los tests automáticamente en cada push |

## Por qué este proyecto

La mayoría de portafolios de QA junior se quedan en pruebas de interfaz y de API. Este proyecto agrega una capa que se prueba con menos frecuencia pero es igual de crítica: verificar que los datos que quedan almacenados sean correctos, consistentes y respeten las reglas del negocio, no solo que la pantalla se vea bien.

Los 10 casos cubren dos tipos de validación:
- **Restricciones de esquema**: la base de datos debe rechazar datos inválidos (emails duplicados, precios negativos, claves foráneas inexistentes) antes de que lleguen a guardarse.
- **Reglas de negocio**: incluso con datos que pasan las restricciones de esquema, se valida que la información tenga sentido (que los totales cuadren, que no existan registros huérfanos).

## Cómo ejecutar las pruebas

```bash
pip install -r requirements.txt
pytest test_database.py -v
```

No se necesita instalar ningún motor de base de datos aparte: SQLite viene incluido en la librería estándar de Python, y cada test corre sobre una base de datos en memoria que se crea y destruye automáticamente.

## Integración continua (CI/CD)

Cada push a la rama `main` dispara la ejecución automática de los 10 tests en GitHub Actions. El resultado se refleja en el badge de arriba.

## Proyectos relacionados

Este repositorio complementa [qa-portfolio-saucedemo](https://github.com/francolondo/qa-portfolio-saucedemo), que cubre pruebas de UI con Selenium y pruebas de API con Postman.
