import matplotlib.pyplot as plt
import numpy as np


class riskProfile:
    def __init__(self, edad, ingreso):
        self.edad = edad
        self.ingreso = ingreso
        self.perfil = self.determinar_perfil()

    def determinar_perfil(self):
        # Perfiles de distribución según edad e ingresos
        if self.ingreso < 30000:  # Bajo ingreso
            if self.edad < 35:
                profile = {'Acciones': 70, 'Bonos': 20, 'Efectivo': 10}  # Agresivo
                self.explicacion = (
                    "Recomendamos este perfil debido a tu capacidad de asumir más riesgos y buscar mayores retornos a largo plazo. "
                    "Una mayor proporción de acciones (stocks) se justifica por tu edad joven. "
                    "Los bonos (bonds) y efectivo (cash) son menores porque hay tiempo para recuperarse de posibles pérdidas."
                )
            elif 35 <= self.edad < 55:
                profile = {'Acciones': 50, 'Bonos': 40, 'Efectivo': 10}  # Moderado
                self.explicacion = (
                    "Recomendamos este perfil debido a que un equilibrio entre acciones y bonos balancea el riesgo y la seguridad. "
                    "Esto es ideal a medida que te acercas a los años de mayor estabilidad financiera. "
                    "El efectivo proporciona liquidez (disponibilidad inmediata de dinero)."
                )
            else:
                profile = {'Acciones': 30, 'Bonos': 60, 'Efectivo': 10}  # Conservador
                self.explicacion = (
                    "Recomendamos este perfil debido a la necesidad de minimizar el riesgo y proteger el capital al acercarte a la jubilación. "
                    "Se sugiere una mayor proporción de bonos (bonds) y una reducción en acciones (stocks) por su mayor volatilidad (variación en el valor)."
                )
        elif 30000 <= self.ingreso < 100000:  # Ingreso medio
            if self.edad < 35:
                profile = {'Acciones': 80, 'Bonos': 15, 'Efectivo': 5}  # Agresivo
                self.explicacion = (
                    "Recomendamos este perfil debido a tu ingreso medio y edad joven, lo que permite una mayor inversión en acciones "
                    "para aprovechar el tiempo y el potencial de crecimiento. "
                    "Los bonos (bonds) y efectivo (cash) son reducidos para maximizar los retornos."
                )
            elif 35 <= self.edad < 55:
                profile = {'Acciones': 60, 'Bonos': 30, 'Efectivo': 10}  # Moderado
                self.explicacion = (
                    "Recomendamos este perfil debido a que un balance entre acciones y bonos es ideal para gestionar el riesgo "
                    "mientras se sigue buscando crecimiento. El efectivo proporciona liquidez para gastos inmediatos."
                )
            else:
                profile = {'Acciones': 40, 'Bonos': 50, 'Efectivo': 10}  # Conservador
                self.explicacion = (
                    "Recomendamos este perfil debido a la proximidad a la jubilación, donde se sugiere incrementar la inversión en bonos "
                    "para reducir el riesgo y proteger los ahorros. Las acciones siguen presentes pero en menor proporción."
                )
        else:  # Alto ingreso
            if self.edad < 35:
                profile = {'Acciones': 85, 'Bonos': 10, 'Efectivo': 5}  # Muy agresivo
                self.explicacion = (
                    "Recomendamos este perfil debido a tus altos ingresos y edad joven, permitiendo maximizar la inversión en acciones "
                    "para lograr el mayor crecimiento posible. Los bonos y efectivo son mínimos debido a tu alta tolerancia al riesgo."
                )
            elif 35 <= self.edad < 55:
                profile = {'Acciones': 65, 'Bonos': 25, 'Efectivo': 10}  # Moderadamente agresivo
                self.explicacion = (
                    "Recomendamos este perfil debido a que tu alto ingreso permite una asignación mayor en acciones mientras "
                    "se mantiene una porción en bonos para estabilidad y efectivo para liquidez."
                )
            else:
                profile = {'Acciones': 45, 'Bonos': 45, 'Efectivo': 10}  # Moderadamente conservador
                self.explicacion = (
                    "Recomendamos este perfil debido a tu alto ingreso y proximidad a la jubilación. "
                    "Se equilibra la inversión entre acciones y bonos para buscar crecimiento mientras se protege el capital. "
                    "El efectivo se mantiene para liquidez."
                )

        return profile

    def graficar_asignacion(self):
        # Graficar la distribución de activos con colores especificados
        labels = self.perfil.keys()
        sizes = self.perfil.values()
        colors = ['darkred', 'lightcoral', 'gray']  # Dark red, light red, gray
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title('Distribución de Activos')
        plt.show()

    def graficar_crecimiento_inversion(self, inversion_inicial=10000, anos=30):
        # Suponer tasas de rendimiento anuales promedio
        rendimiento = {
            'Acciones': 0.08,  # 8% anual
            'Bonos': 0.04,  # 4% anual
            'Efectivo': 0.02  # 2% anual
        }

        # Calcular crecimiento teórico usando capitalización compuesta
        anos_array = np.arange(1, anos + 1)
        valor = inversion_inicial
        crecimiento = [valor]  # Incluir valor inicial

        for ano in anos_array[1:]:
            valor_anterior = valor
            # Actualizar valor según el rendimiento y el porcentaje de cada activo
            for tipo, porcentaje in self.perfil.items():
                valor += valor_anterior * (rendimiento[tipo] * porcentaje / 100)
            crecimiento.append(valor)

        # Graficar crecimiento de la inversión
        plt.figure(figsize=(10, 6))
        plt.plot(anos_array, crecimiento, marker='o')
        plt.title('Crecimiento Teórico de la Inversión')
        plt.xlabel('Años')
        plt.ylabel('Valor de la Inversión')
        plt.grid(True)
        plt.show()

    def get_explicacion(self):
        return(self.explicacion)


# Ejemplo de uso
# perfil_inversionista = riskProfile(edad=30, ingreso=50000)
#
# # Mostrar la explicación del perfil
# perfil_inversionista.mostrar_explicacion()
#
# # Graficar la asignación de activos
# perfil_inversionista.graficar_asignacion()
#
# # Graficar crecimiento teórico de la inversión
# perfil_inversionista.graficar_crecimiento_inversion(inversion_inicial=10000, anos=30)
