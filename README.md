# ITESO-software-design-examen-2

## **Ejercicio 1 – Sistema de Notificaciones de Pedidos**

### **Problema original**

El código mezclaba:

* Lógica de impresión
* Lógica de negocio
* Lógica de cada tipo de notificación
* Selección del tipo de notificación con `if-elif`
* Falta de separación correcta por responsabilidades

Esto dificultaba la extensión y violaba OCP y SRP.

### **Principios SOLID aplicados**

* **SRP:**

  * `OrderProcessor` procesa pedidos.
  * `HistoryManager` guarda historial.
  * Cada estrategia maneja su propia notificación.

* **OCP:**

  * Nuevos tipos de notificación se agregan creando nuevas estrategias sin modificar código existente.

* **DIP:**

  * El procesador depende de la abstracción `NotificationStrategy`, no de las implementaciones concretas.

### **Patrones aplicados**

* **Strategy:**

  * `NotificationStrategy` + `EmailNotification`, `SMSNotification`, `PushNotification`.

* **Factory:**

  * `NotificationFactory` crea la estrategia según el tipo.

* **Clase OrderInfo:**

  * `OrderInfo` encapsula todos los datos usados por las estrategias.

### **Mejoras**

* Extensible sin modificar código existente.
* Eliminación de condicionales.
* Estructura flexible y fácil de mantener.

### **Diagramas generados**

* C1 – Contexto
* C2 – Contenedores
* C3 – Componentes
* C4 – Código

---

## **Ejercicio 2 – Sistema de Generación de Reportes**

### **Problema original**

* Lógica de 3 reportes mezclada en un solo método.
* Lógica de formato incrustada.
* Lógica de entrega acoplada.
* Uso excesivo de `if-elif`.
* Código monolítico difícil de extender.

### **Principios SOLID aplicados**

* **SRP:**

  * Cada tipo de reporte tiene su propia clase.
  * Formatter y Delivery tienen responsabilidades separadas.
  * `ReportSystem` solo orquesta.

* **OCP:**

  * Nuevos reportes, formatos o entregas se agregan sin modificar código existente.

* **DIP:**

  * `ReportSystem` depende de abstracciones (`ReportStrategy`, `FormatStrategy`, `DeliveryStrategy`).

### **Patrones aplicados**

* **Template Method:**

  * `ReportStrategy.generate()` define la estructura.
  * Subclases implementan `title()` `body()`.

* **Builder:**

  * `ReportBuilder` construye el contenido sin concatenación manual.

* **Strategy:**

  * `FormatStrategy` (PDF/Excel/HTML).
  * `DeliveryStrategy` (Email/Download/Cloud).
  * `ReportStrategy` (Sales/Inventory/Financial).

* **Factory:**

  * `ReportFactory`, `FormatFactory`, `DeliveryFactory`.

### **Mejoras**

* Código modular, extensible y sin condicionales.
* Separación clara de responsabilidades.
* Flexibilidad para agregar nuevas salidas y reportes.

### **Diagramas generados**

* C1 – Contexto
* C2 – Contenedores
* C3 – Componentes
* C4 – Código

---

## **Ejecución**

Ambos ejercicios pueden ejecutarse con:

```
python ejercicioX.py
```

---

## **Conclusión**

Ambos códigos fueron refactorizados aplicando:

* Principios SOLID
* Strategy
* Factory
* Template Method (Ejercicio 2)
* Builder (Ejercicio 2)
* Clase OrderInfo (Ejercicio 1)

La arquitectura resultante es más mantenible, extensible y alineada con las buenas prácticas.
