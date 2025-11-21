from datetime import datetime
import json


# ============================================================
# Builder simple para evitar concatenaciones manuales
# ============================================================

class ReportBuilder:
    def __init__(self):
        self.parts = []

    def add(self, text: str):
        self.parts.append(text + "\n")
        return self

    def separator(self):
        self.parts.append("-" * 60 + "\n")
        return self

    def header(self, title: str):
        self.parts.append("=" * 60 + "\n")
        self.parts.append(f"           {title}\n")
        self.parts.append("=" * 60 + "\n")
        return self

    def build(self):
        return "".join(self.parts)


# ============================================================
# Template Method para generación de contenido de reporte
# ============================================================

class ReportStrategy:
    """
    Template Method:
    - generate() define el paso general
    - header() y body() son sobreescritos por subclases
    """

    def generate(self, data, timestamp: str) -> str:
        builder = ReportBuilder()
        builder.header(self.title())
        builder.add(f"Fecha de generación: {timestamp}\n")
        self.body(builder, data)
        return builder.build()

    def title(self):
        raise NotImplementedError

    def body(self, builder: ReportBuilder, data):
        raise NotImplementedError


# ============================================================
# Estrategias concretas usando Template Method + Builder 
# ============================================================

class SalesReport(ReportStrategy):
    def title(self):
        return "REPORTE DE VENTAS"

    def body(self, builder, data):
        total_sales = sum(item['amount'] for item in data['sales'])

        builder.add(f"Total de ventas: ${total_sales:.2f}")
        builder.add(f"Número de transacciones: {len(data['sales'])}")
        builder.add(f"Periodo: {data['period']}\n")

        builder.add("Detalle de ventas:")
        builder.separator()

        for sale in data['sales']:
            builder.add(f"  • Producto: {sale['product']} - ${sale['amount']:.2f}")


class InventoryReport(ReportStrategy):
    def title(self):
        return "REPORTE DE INVENTARIO"

    def body(self, builder, data):
        total_items = sum(item['quantity'] for item in data['items'])
        categories = len(set(item['category'] for item in data['items']))

        builder.add(f"Total de productos: {total_items}")
        builder.add(f"Categorías: {categories}\n")

        builder.add("Inventario actual:")
        builder.separator()

        for item in data['items']:
            builder.add(
                f"  • {item['name']} ({item['category']}): {item['quantity']} unidades"
            )


class FinancialReport(ReportStrategy):
    def title(self):
        return "REPORTE FINANCIERO"

    def body(self, builder, data):
        income = data['income']
        expenses = data['expenses']
        balance = income - expenses

        builder.add(f"Ingresos: ${income:.2f}")
        builder.add(f"Gastos: ${expenses:.2f}")
        builder.add(f"Balance: ${balance:.2f}")


# ============================================================
# Estrategias de formato (Strategy)
# ============================================================

class FormatStrategy:
    def format(self, content: str) -> str:
        raise NotImplementedError


class PDFFormatter(FormatStrategy):
    def format(self, content: str) -> str:
        print("📄 Generando reporte en formato PDF...")
        return f"[PDF FORMAT]\n{content}\n[END PDF]"


class ExcelFormatter(FormatStrategy):
    def format(self, content: str) -> str:
        print("📊 Generando reporte en formato Excel...")
        return f"[EXCEL FORMAT]\n{content}\n[END EXCEL]"


class HTMLFormatter(FormatStrategy):
    def format(self, content: str) -> str:
        print("🌐 Generando reporte en formato HTML...")
        return f"<html><body><pre>\n{content}\n</pre></body></html>"


# ============================================================
# Estrategias de entrega (Strategy)
# ============================================================

class DeliveryStrategy:
    def deliver(self, formatted_report: str, report_type: str, output_format: str):
        raise NotImplementedError


class EmailDelivery(DeliveryStrategy):
    def deliver(self, formatted_report: str, report_type: str, output_format: str):
        print("📧 Enviando reporte por email...")
        print("   Destinatario: admin@company.com")


class DownloadDelivery(DeliveryStrategy):
    def deliver(self, formatted_report: str, report_type: str, output_format: str):
        filename = (
            f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            f".{output_format}"
        )
        print("💾 Reporte disponible para descarga:")
        print(f"   Archivo: {filename}")


class CloudDelivery(DeliveryStrategy):
    def deliver(self, formatted_report: str, report_type: str, output_format: str):
        print("☁️  Subiendo reporte a la nube...")
        print(f"   URL: https://cloud.company.com/reports/{report_type}")


# ============================================================
# Factories
# ============================================================

class ReportFactory:
    _strategies = {
        'sales': SalesReport,
        'inventory': InventoryReport,
        'financial': FinancialReport
    }

    @staticmethod
    def create(report_type: str) -> ReportStrategy:
        cls = ReportFactory._strategies.get(report_type)
        if not cls:
            raise ValueError(f"Tipo de reporte desconocido: {report_type}")
        return cls()


class FormatFactory:
    _strategies = {
        'pdf': PDFFormatter,
        'excel': ExcelFormatter,
        'html': HTMLFormatter
    }

    @staticmethod
    def create(output_format: str) -> FormatStrategy:
        cls = FormatFactory._strategies.get(output_format)
        if not cls:
            raise ValueError(f"Formato desconocido: {output_format}")
        return cls()


class DeliveryFactory:
    _strategies = {
        'email': EmailDelivery,
        'download': DownloadDelivery,
        'cloud': CloudDelivery
    }

    @staticmethod
    def create(delivery_method: str) -> DeliveryStrategy:
        cls = DeliveryFactory._strategies.get(delivery_method)
        if not cls:
            raise ValueError(f"Método de entrega desconocido: {delivery_method}")
        return cls()


# ============================================================
# Historial
# ============================================================

class HistoryManager:
    def __init__(self):
        self._reports = []

    def save(self, record: dict):
        self._reports.append(record)

    def get_all(self):
        return self._reports


# ============================================================
# Sistema principal
# ============================================================

class ReportSystem:
    def __init__(self):
        self.history = HistoryManager()

    def generate_report(self, report_type, data, output_format, delivery_method):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_strategy = ReportFactory.create(report_type)
        format_strategy = FormatFactory.create(output_format)
        delivery_strategy = DeliveryFactory.create(delivery_method)

        report_content = report_strategy.generate(data, timestamp)
        formatted_report = format_strategy.format(report_content)
        delivery_strategy.deliver(formatted_report, report_type, output_format)

        self.history.save({
            'type': report_type,
            'format': output_format,
            'delivery': delivery_method,
            'timestamp': timestamp
        })

        print("\n✅ Reporte generado exitosamente\n")
        print(formatted_report)
        print("\n" + "=" * 60 + "\n")

        return formatted_report

    def get_report_history(self):
        return self.history.get_all()


# ============================================================
# Código de prueba
# ============================================================

if __name__ == "__main__":
    system = ReportSystem()

    # Reporte de ventas
    sales_data = {
        'period': 'Enero 2024',
        'sales': [
            {'product': 'Laptop HP', 'amount': 899.99},
            {'product': 'Mouse Logitech', 'amount': 25.50},
            {'product': 'Teclado Mecánico', 'amount': 120.00},
            {'product': 'Monitor LG 24"', 'amount': 199.99}
        ]
    }

    system.generate_report('sales', sales_data, 'pdf', 'email')

    # Reporte de inventario
    inventory_data = {
        'items': [
            {'name': 'Laptop HP', 'category': 'Computadoras', 'quantity': 15},
            {'name': 'Mouse Logitech', 'category': 'Accesorios', 'quantity': 50},
            {'name': 'Teclado Mecánico', 'category': 'Accesorios', 'quantity': 30},
            {'name': 'Monitor LG', 'category': 'Pantallas', 'quantity': 20}
        ]
    }

    system.generate_report('inventory', inventory_data, 'excel', 'download')

    # Reporte financiero
    financial_data = {
        'income': 50000.00,
        'expenses': 32000.00
    }

    system.generate_report('financial', financial_data, 'html', 'cloud')

    # Mostrar historial
    print("\nHISTORIAL DE REPORTES GENERADOS:")
    print(json.dumps(system.get_report_history(), indent=2, ensure_ascii=False))
