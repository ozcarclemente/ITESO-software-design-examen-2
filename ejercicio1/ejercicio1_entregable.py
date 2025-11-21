from datetime import datetime
import json


# ============================================================
# Clase para encapsular datos comunes del pedido (Value Object)
# ============================================================

class OrderInfo:
    def __init__(self, order_data):
        self.customer = order_data["customer"]
        self.order_id = order_data["order_id"]
        self.total = order_data["total"]

        self.name = self.customer["name"]
        self.email = self.customer["email"]
        self.phone = self.customer["phone"]
        self.device = self.customer["device_id"]


# ============================================================
# Estrategia base
# ============================================================

class NotificationStrategy:
    def send(self, info: OrderInfo):
        raise NotImplementedError


# ============================================================
# Estrategias concretas
# ============================================================

class EmailNotification(NotificationStrategy):
    def send(self, info: OrderInfo):

        message = (
            f"Estimado {info.name}, su pedido #{info.order_id} por ${info.total} ha sido confirmado."
        )

        print(f"📧 EMAIL enviado a {info.email}")
        print(f"   Asunto: Confirmación de Pedido #{info.order_id}")
        print(f"   Mensaje: {message}\n")

        return {
            'type': 'email',
            'to': info.email,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }


class SMSNotification(NotificationStrategy):
    def send(self, info: OrderInfo):

        message = (
            f"Pedido #{info.order_id} confirmado. Total: ${info.total}. Gracias por su compra!"
        )

        print(f"📱 SMS enviado a {info.phone}")
        print(f"   Mensaje: {message}\n")

        return {
            'type': 'sms',
            'to': info.phone,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }


class PushNotification(NotificationStrategy):
    def send(self, info: OrderInfo):

        message = f"¡Pedido confirmado! #{info.order_id} - ${info.total}"

        print(f"🔔 PUSH enviada al dispositivo {info.device}")
        print(f"   Mensaje: {message}\n")

        return {
            'type': 'push',
            'to': info.device,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }


# ============================================================
# Factory de estrategias
# ============================================================

class NotificationFactory:
    _strategies = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification
    }

    @staticmethod
    def create(notification_type):
        cls = NotificationFactory._strategies.get(notification_type)
        if not cls:
            raise ValueError(f"Tipo de notificación desconocido: {notification_type}")
        return cls()


# ============================================================
# Historial
# ============================================================

class HistoryManager:
    def __init__(self):
        self.notifications = []

    def save(self, notification_record):
        self.notifications.append(notification_record)

    def get_all(self):
        return self.notifications


# ============================================================
# Procesador principal
# ============================================================

class OrderProcessor:
    def __init__(self):
        self.history = HistoryManager()

    def process_order(self, order_data, notification_types):

        info = OrderInfo(order_data)

        print(f"\n{'='*50}")
        print(f"Procesando pedido #{info.order_id}")
        print(f"Cliente: {info.name}")
        print(f"Total: ${info.total}")
        print(f"{'='*50}\n")

        for notif_type in notification_types:
            strategy = NotificationFactory.create(notif_type)
            record = strategy.send(info)
            self.history.save(record)

    def get_history(self):
        return self.history.get_all()


# ============================================================
# Pruebas
# ============================================================

if __name__ == "__main__":
    system = OrderProcessor()

    # Pedido 1: Cliente premium
    order1 = {
        'order_id': 'ORD-001',
        'customer': {
            'name': 'Ana García',
            'email': 'ana.garcia@email.com',
            'phone': '+34-600-123-456',
            'device_id': 'DEVICE-ABC-123'
        },
        'total': 150.50
    }

    system.process_order(order1, ['email', 'sms', 'push'])

    # Pedido 2: Cliente estándar
    order2 = {
        'order_id': 'ORD-002',
        'customer': {
            'name': 'Carlos Ruiz',
            'email': 'carlos.ruiz@email.com',
            'phone': '+34-600-789-012',
            'device_id': 'DEVICE-XYZ-789'
        },
        'total': 75.00
    }

    system.process_order(order2, ['email'])

    # Mostrar historial
    print("\n" + "="*50)
    print("HISTORIAL DE NOTIFICACIONES")
    print("="*50)
    print(json.dumps(system.get_history(), indent=2, ensure_ascii=False))
