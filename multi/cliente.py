import asyncio
import random

class AgenteCliente:
    def __init__(self, nombre, prioridad, server_ip):
        self.nombre = nombre
        self.prioridad = prioridad
        self.server_ip = server_ip
        self.activo = True  # Estado inicial

    async def solicitar_recurso(self):
        # Si el agente ha fallado, no solicita el recurso
        if not self.activo:
            print(f"{self.nombre} está inactivo y no puede solicitar el recurso en este momento.")
            return

        reader, writer = await asyncio.open_connection(self.server_ip, 8888)
        print(f"{self.nombre} está solicitando el recurso.")
        mensaje = f"{self.nombre},{self.prioridad}"
        writer.write(mensaje.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f"{self.nombre} recibe: {data.decode().strip()}")

        writer.close()
        await writer.wait_closed()

    def verificar_fallo(self):
        if random.random() < 0.2:  # 20% de probabilidad de fallo
            self.activo = False
            print(f"{self.nombre} ha fallado y está inactivo.")
        elif not self.activo:
            # Probabilidad de reactivarse en la siguiente ronda
            if random.random() < 0.5:
                self.activo = True
                print(f"{self.nombre} se ha recuperado y vuelve a estar activo.")

async def main():
    server_ip = input("Ingrese la IP del servidor: ")
    nombre_agente = input("Ingrese el nombre del agente: ")
    prioridad = int(input("Ingrese la prioridad del agente (1-10): "))

    agente = AgenteCliente(nombre_agente, prioridad, server_ip)

    while True:
        agente.verificar_fallo()  # Verifica si el agente falla o se recupera
        if agente.activo:
            await agente.solicitar_recurso()
        # Pausa aleatoria entre solicitudes o intentos de recuperación
        await asyncio.sleep(random.uniform(2, 5))

asyncio.run(main())
