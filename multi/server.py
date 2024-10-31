import asyncio
import random

class RecursoServidor:
    def __init__(self):
        self.disponible = True
        self.usuario_actual = None

    async def manejar_solicitud(self, reader, writer):
        data = await reader.read(100)
        mensaje = data.decode().strip().split(",")
        nombre_agente = mensaje[0]
        prioridad = int(mensaje[1])

        print(f"{nombre_agente} (Prioridad {prioridad}) solicita el recurso.")
        
        if self.disponible:
            self.disponible = False
            self.usuario_actual = (nombre_agente, prioridad)
            response = f"Recurso asignado a {nombre_agente} (Prioridad {prioridad}).\n"
        else:
            actual_nombre, actual_prioridad = self.usuario_actual
            if prioridad > actual_prioridad:
                print(f"{nombre_agente} tiene mayor prioridad que {actual_nombre}. Negociando...")
                response = f"{actual_nombre} libera el recurso. {nombre_agente} toma el recurso.\n"
                self.usuario_actual = (nombre_agente, prioridad)
            else:
                response = f"{nombre_agente} espera porque {actual_nombre} tiene igual o mayor prioridad.\n"

        writer.write(response.encode())
        await writer.drain()

        # Simula el uso del recurso durante 2 segundos antes de liberarlo
        await asyncio.sleep(2)
        if self.usuario_actual[0] == nombre_agente:
            self.disponible = True
            print(f"Recurso liberado por {nombre_agente}.")
            writer.write("Recurso liberado.\n".encode())
            await writer.drain()

        writer.close()

async def main():
    server = await asyncio.start_server(RecursoServidor().manejar_solicitud, '0.0.0.0', 8888)
    print("Servidor ejecutándose en el puerto 8888...")
    async with server:
        await server.serve_forever()

asyncio.run(main())
