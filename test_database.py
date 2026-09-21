"""
Pruebas de integridad de base de datos con SQLite y pytest.

Valida tanto restricciones estructurales del esquema (UNIQUE, CHECK,
FOREIGN KEY) como reglas de negocio sobre los datos, según el plan de
pruebas en casos_de_prueba_sql.md (CP-01 a CP-10).

Requisitos:
    pip install pytest
    (sqlite3 viene incluido en la librería estándar de Python, no
    requiere instalar ningún motor de base de datos aparte)

Cómo correr los tests:
    pytest test_database.py -v
"""

import sqlite3
import pytest


@pytest.fixture
def db():
    """
    Crea una base de datos SQLite nueva en memoria para cada test,
    a partir de schema.sql. Al ser en memoria, cada test arranca
    con una base de datos limpia y no deja archivos residuales.
    """
    conexion = sqlite3.connect(":memory:")
    conexion.execute("PRAGMA foreign_keys = ON")

    with open("schema.sql", "r", encoding="utf-8") as archivo:
        conexion.executescript(archivo.read())

    yield conexion
    conexion.close()


def crear_usuario(db, nombre="Ana Pérez", email="ana@example.com"):
    cursor = db.execute(
        "INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email)
    )
    db.commit()
    return cursor.lastrowid


def crear_producto(db, nombre="Camiseta", precio=25.0, stock=10):
    cursor = db.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock),
    )
    db.commit()
    return cursor.lastrowid


# ---------- CP-01: Crear usuario con datos válidos ----------
def test_crear_usuario_valido(db):
    usuario_id = crear_usuario(db)
    fila = db.execute(
        "SELECT nombre, email FROM usuarios WHERE id = ?", (usuario_id,)
    ).fetchone()
    assert fila == ("Ana Pérez", "ana@example.com")


# ---------- CP-02: Rechazar email duplicado ----------
def test_email_duplicado_falla(db):
    crear_usuario(db, email="duplicado@example.com")
    with pytest.raises(sqlite3.IntegrityError):
        crear_usuario(db, nombre="Otro Usuario", email="duplicado@example.com")


# ---------- CP-03: Rechazar producto con precio negativo ----------
def test_producto_precio_negativo_falla(db):
    with pytest.raises(sqlite3.IntegrityError):
        crear_producto(db, precio=-10)


# ---------- CP-04: Rechazar producto con stock negativo ----------
def test_producto_stock_negativo_falla(db):
    with pytest.raises(sqlite3.IntegrityError):
        crear_producto(db, stock=-5)


# ---------- CP-05: Crear pedido para un usuario existente ----------
def test_crear_pedido_usuario_existente(db):
    usuario_id = crear_usuario(db)
    cursor = db.execute(
        "INSERT INTO pedidos (usuario_id, estado) VALUES (?, 'pendiente')",
        (usuario_id,),
    )
    db.commit()
    assert cursor.lastrowid is not None


# ---------- CP-06: Rechazar pedido con usuario inexistente ----------
def test_pedido_usuario_inexistente_falla(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO pedidos (usuario_id, estado) VALUES (9999, 'pendiente')"
        )
        db.commit()


# ---------- CP-07: Rechazar item de pedido con cantidad inválida ----------
def test_item_cantidad_invalida_falla(db):
    usuario_id = crear_usuario(db)
    producto_id = crear_producto(db)
    pedido_id = db.execute(
        "INSERT INTO pedidos (usuario_id) VALUES (?)", (usuario_id,)
    ).lastrowid
    db.commit()

    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unitario) "
            "VALUES (?, ?, 0, 25.0)",
            (pedido_id, producto_id),
        )
        db.commit()


# ---------- CP-08: Rechazar estado de pedido inválido ----------
def test_estado_pedido_invalido_falla(db):
    usuario_id = crear_usuario(db)
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO pedidos (usuario_id, estado) VALUES (?, 'inventado')",
            (usuario_id,),
        )
        db.commit()


# ---------- CP-09: El total del pedido coincide con la suma de sus items ----------
def test_total_pedido_coincide_con_items(db):
    usuario_id = crear_usuario(db)
    producto_id = crear_producto(db, precio=25.0)
    pedido_id = db.execute(
        "INSERT INTO pedidos (usuario_id) VALUES (?)", (usuario_id,)
    ).lastrowid

    items = [(pedido_id, producto_id, 2, 25.0), (pedido_id, producto_id, 1, 25.0)]
    db.executemany(
        "INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unitario) "
        "VALUES (?, ?, ?, ?)",
        items,
    )
    db.commit()

    total = db.execute(
        "SELECT SUM(cantidad * precio_unitario) FROM pedido_items WHERE pedido_id = ?",
        (pedido_id,),
    ).fetchone()[0]

    total_esperado = sum(cantidad * precio for _, _, cantidad, precio in items)
    assert total == total_esperado


# ---------- CP-10: No existen items de pedido huérfanos ----------
def test_no_hay_items_huerfanos(db):
    usuario_id = crear_usuario(db)
    producto_id = crear_producto(db)
    pedido_id = db.execute(
        "INSERT INTO pedidos (usuario_id) VALUES (?)", (usuario_id,)
    ).lastrowid
    db.execute(
        "INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unitario) "
        "VALUES (?, ?, 1, 25.0)",
        (pedido_id, producto_id),
    )
    db.commit()

    huerfanos = db.execute(
        """
        SELECT pi.id FROM pedido_items pi
        LEFT JOIN productos p ON pi.producto_id = p.id
        WHERE p.id IS NULL
        """
    ).fetchall()

    assert len(huerfanos) == 0
