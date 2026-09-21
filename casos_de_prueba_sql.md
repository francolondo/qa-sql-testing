# Plan de Pruebas — Base de Datos (SQLite)

Valida tanto las restricciones estructurales del esquema (`schema.sql`) como reglas de negocio sobre los datos.

---

## CP-01 — Crear usuario con datos válidos
| Campo | Detalle |
|---|---|
| Pasos | Insertar un usuario con nombre y email únicos |
| Resultado esperado | El registro se inserta correctamente y se le asigna un `id` autoincremental |

## CP-02 — Rechazar email duplicado
| Campo | Detalle |
|---|---|
| Pasos | Insertar dos usuarios con el mismo email |
| Resultado esperado | La segunda inserción falla con `IntegrityError` por violar la restricción `UNIQUE` |

## CP-03 — Rechazar producto con precio negativo
| Campo | Detalle |
|---|---|
| Pasos | Insertar un producto con `precio = -10` |
| Resultado esperado | Falla por violar la restricción `CHECK (precio >= 0)` |

## CP-04 — Rechazar producto con stock negativo
| Campo | Detalle |
|---|---|
| Pasos | Insertar un producto con `stock = -5` |
| Resultado esperado | Falla por violar la restricción `CHECK (stock >= 0)` |

## CP-05 — Crear pedido para un usuario existente
| Campo | Detalle |
|---|---|
| Pasos | Insertar un pedido con `usuario_id` de un usuario ya existente |
| Resultado esperado | El pedido se inserta correctamente |

## CP-06 — Rechazar pedido con usuario inexistente
| Campo | Detalle |
|---|---|
| Pasos | Insertar un pedido con `usuario_id = 9999` (no existe) |
| Resultado esperado | Falla por violar la restricción `FOREIGN KEY` |

## CP-07 — Rechazar item de pedido con cantidad inválida
| Campo | Detalle |
|---|---|
| Pasos | Insertar un `pedido_item` con `cantidad = 0` |
| Resultado esperado | Falla por violar la restricción `CHECK (cantidad > 0)` |

## CP-08 — Rechazar estado de pedido inválido
| Campo | Detalle |
|---|---|
| Pasos | Insertar un pedido con `estado = 'inventado'` |
| Resultado esperado | Falla por violar la restricción `CHECK` de valores permitidos |

## CP-09 — El total del pedido coincide con la suma de sus items
| Campo | Detalle |
|---|---|
| Pasos | Crear un pedido con 3 items, calcular `SUM(cantidad * precio_unitario)` |
| Resultado esperado | El total calculado coincide exactamente con la suma esperada |

## CP-10 — No existen items de pedido huérfanos
| Campo | Detalle |
|---|---|
| Pasos | Consultar `pedido_items` cuyo `producto_id` no exista en `productos` |
| Resultado esperado | La consulta devuelve 0 filas (integridad referencial de datos, no solo de esquema) |
