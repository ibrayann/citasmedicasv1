from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotFound, HttpResponseRedirect 
from django.shortcuts import render
import aiohttp
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.views.decorators.http import require_http_methods
import asyncio
from django.urls import reverse
from django.shortcuts import render
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

async def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data)

        endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/login'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint_url, data=json_data, headers=headers) as response:
                    if response.status == 200:
                        try:
                            response_json = await response.json()
                            
                            # Realiza acciones adicionales con response_json si es necesario
                            
                            # Guarda el contenido en el localStorage
                            # Esta parte se debe realizar en JavaScript en el cliente
                            # Aquí solo puedes indicar qué hacer en la respuesta exitosa
                            return JsonResponse(response_json, status=200)
                        except Exception as e:
                            # Maneja errores al cargar JSON
                            print(f"Error al cargar JSON: {e}")
                            return HttpResponseServerError()
                    elif response.status == 404:
                        # Usuario no registrado en el sistema externo
                        return JsonResponse({'message': 'Usuario no registrado'}, status=404)
                    elif response.status == 401:
                        # Credenciales inválidas en el sistema externo
                        return JsonResponse({'message': 'Credenciales inválidas'}, status=401)
                    else:
                        # Otro error inesperado en la solicitud
                        return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
        except Exception as e:
            # Maneja errores de solicitud
            print(f"Error en la solicitud: {e}")
            return HttpResponseServerError()

    # Si la solicitud es GET, muestra la plantilla 'login.html'
    return render(request, 'login.html')


async def register(request):
    if request.method == 'POST':
        run_paciente = request.POST.get('rut')
        nombre = request.POST.get('name')
        apellido = request.POST.get('lastname')
        telefono = request.POST.get('phone')
        direccion = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {
            'run_paciente': run_paciente,
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'direccion': direccion,
            'email': email,
            'password': password
        }
        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data)

        endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes/add_paciente'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint_url, data=json_data, headers=headers) as response:
                    if response.status == 201:
                        try:
                            response_json = await response.json()
                            
                            # Realiza acciones adicionales con response_json si es necesario
                            
                            # Guarda el contenido en el localStorage
                            # Esta parte se debe realizar en JavaScript en el cliente
                            # Aquí solo puedes indicar qué hacer en la respuesta exitosa
                            return JsonResponse(response_json, status=201)
                        except Exception as e:
                            # Maneja errores al cargar JSON
                            print(f"Error al cargar JSON: {e}")
                            return HttpResponseServerError()
                    elif response.status == 500:
                        # Usuario no registrado en el sistema externo
                        return JsonResponse({'message': 'Usuario no registrado, verifique email o rut no esten asociados a una cuenta'}, status=404)
                    else:
                        # Otro error inesperado en la solicitud
                        return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
                    
        except Exception as e:
            # Maneja errores de solicitud
            print(f"Error en la solicitud: {e}")
            return HttpResponseServerError()

    # Si la solicitud es GET, muestra la plantilla 'login.html'
    return render(request, 'register.html')

async def pacientes(request):
    # Realiza una solicitud GET a la URL externa 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'
    endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        print(response_json)

                        # Procesa los datos recibidos según sea necesario
                        # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                        # Obtener datos específicos del JSON de respuesta
                        pacientes_data = response_json
                        # Establecer esos datos en el contexto

                        # Luego renderiza la plantilla pacientes.html con los datos
                        return render(request, 'pacientes.html', {'pacientes_data': pacientes_data})


                    except Exception as e:
                        # Maneja errores al cargar JSON
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    # Otro error inesperado en la solicitud
                    return HttpResponseServerError()

    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()


def home(request):
    return render(request, 'home.html')

def logout(request):
    return render(request, 'logout.html')

async def medicos(request):
    # Realiza una solicitud GET a la URL externa 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'
    endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/medicos'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        # Procesa los datos recibidos según sea necesario
                        # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                        # Obtener datos específicos del JSON de respuesta
                        medicos_data = response_json
                        # Establecer esos datos en el contexto

                        # Luego renderiza la plantilla pacientes.html con los datos
                        return render(request, 'medicos.html', {'medicos_data': medicos_data})


                    except Exception as e:
                        # Maneja errores al cargar JSON
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    # Otro error inesperado en la solicitud
                    return HttpResponseServerError()

    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()

async def agendamedica(request, run):
    # Realiza una solicitud GET a la URL externa 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'
    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/run-medico/{run}'


    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        # Procesa los datos recibidos según sea necesario
                        # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                        # Obtener datos específicos del JSON de respuesta
                        agendamedica_data = response_json
                        # Establecer esos datos en el contexto
                        if len(response_json) > 0:
                            # Procesa los datos recibidos según sea necesario
                            # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                            # Obtener datos específicos del JSON de respuesta
                            agendamedica_data = response_json

                            # Luego renderiza la plantilla agendamedica.html con los datos
                            return render(request, 'agendamedica.html', {'agendamedica_data': agendamedica_data, 'run': agendamedica_data[0]['run_medico']})
                        else:
                            print('no hay datos')
                            print(run)
                            return render(request, 'agendamedica.html', { 'run': str(run)})
                        
                
                    except Exception as e:
                        # Maneja errores al cargar JSON
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    # Otro error inesperado en la solicitud
                    return []

    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()

# En tu archivo views.py

async def agregardia(request, run):
    if run:
        if request.method == 'POST':
            fecha = request.POST.get('fecha')
            data = {'fecha': fecha, 'run_medico': run}
            headers = {'Content-Type': 'application/json'}
            json_data = json.dumps(data)

            endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/agregar-dia'
            print('data',data)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(endpoint_url, data=json_data, headers=headers) as response:
                        if response.status == 200:
                            try:
                                response_json = await response.json()
                                return HttpResponseRedirect(reverse('agendamedica', args=(run,)))
                            except Exception as e:
                                print(f"Error al cargar JSON: {e}")
                                return HttpResponseServerError()
                        elif response.status == 404:
                            return JsonResponse({'message': 'Usuario no registrado'}, status=404)
                        else:
                            return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
            except Exception as e:
                # Maneja errores de solicitud
                print(f"Error en la solicitud: {e}")
                return HttpResponseServerError()
    else:
        return HttpResponseNotFound()

async def cambioDisponibilidad(request):

    id_agenda = request.POST.get('agenda_id')
    disponible = request.POST.get('disponible')
    json_data = {'disponible': disponible }
    headers = {'Content-Type': 'application/json'}
    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/desbloquear-hora/{id_agenda}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(endpoint_url, json=json_data, headers=headers) as response:
                print(response)
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        return HttpResponseRedirect(reverse('medicos'))
                    except Exception as e:
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                elif response.status == 404:
                    return JsonResponse({'message': 'Usuario no registrado'}, status=404)
                else:
                    return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()


async def registermedico(request):
    if request.method == 'POST':
        run_paciente = request.POST.get('rut')
        nombre = request.POST.get('name')
        apellido = request.POST.get('lastname')
        telefono = request.POST.get('phone')
        direccion = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        especialidad = request.POST.get('especialidad')
        sucursal = request.POST.get('sucursal')
        run_secretaria = request.POST.get('run_secretaria')

        data = {
            'run_medico': run_paciente,
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'direccion': direccion,
            'email': email,
            'password': password,
            'ID_especialidad': especialidad,
            'ID_sucursal': sucursal,
            'Run_secretaria': run_secretaria
        }
        print(data)
        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data)

        endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/medicos/add_medico'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint_url, data=json_data, headers=headers) as response:
                    if response.status == 201:
                        try:
                            response_json = await response.json()
                            
                            # Realiza acciones adicionales con response_json si es necesario
                            
                            # Guarda el contenido en el localStorage
                            # Esta parte se debe realizar en JavaScript en el cliente
                            # Aquí solo puedes indicar qué hacer en la respuesta exitosa
                            return JsonResponse(response_json, status=201)
                        except Exception as e:
                            # Maneja errores al cargar JSON
                            print(f"Error al cargar JSON: {e}")
                            return HttpResponseServerError()
                    elif response.status == 500:
                        # Usuario no registrado en el sistema externo
                        return JsonResponse({'message': 'Usuario no registrado, verifique email o rut no esten asociados a una cuenta'}, status=404)
                    else:
                        # Otro error inesperado en la solicitud
                        return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
                    
        except Exception as e:
            # Maneja errores de solicitud
            print(f"Error en la solicitud: {e}")
            return HttpResponseServerError()

    # Si la solicitud es GET, muestra la plantilla 'login.html'
    return render(request, 'registermedico.html')

async def citas_medicas(request):
        # Realiza una solicitud GET a la URL externa 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'
    endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/citasmedicas/'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        # Procesa los datos recibidos según sea necesario
                        # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                        # Obtener datos específicos del JSON de respuesta
                        citas_data = response_json
                        # Establecer esos datos en el contexto

                        # Luego renderiza la plantilla pacientes.html con los datos
                        return render(request, 'citas.html', {'citas_data': citas_data})


                    except Exception as e:
                        # Maneja errores al cargar JSON
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    # Otro error inesperado en la solicitud
                    return HttpResponseServerError()

    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()

async def anular_cita(request, ID_agenda):
    disponible = True
    json_data = {'disponible': disponible }
    headers = {'Content-Type': 'application/json'}
    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/desbloquear-hora/{ID_agenda}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(endpoint_url, json=json_data, headers=headers) as response:
                print(response)
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        return render(request, 'citas.html')
                    except Exception as e:
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                elif response.status == 404:
                    return JsonResponse({'message': 'Usuario no registrado'}, status=404)
                else:
                    return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
                
    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()
    
    


async def formulario_cita(request):
    return  render(request,'formulario_cita.html')
    

async def agendarhora(request):
    sucursal = request.GET.get('sucursal')
    especialidad = request.GET.get('especialidad')
    # Realiza una solicitud GET a la URL externa 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'
    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/medicos/medicos_sucursal_especialidad/{sucursal}/{especialidad}'
    print(sucursal)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        # Procesa los datos recibidos según sea necesario
                        # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                        # Obtener datos específicos del JSON de respuesta
                        medicos_data = response_json
                        print(medicos_data)
                        # Establecer esos datos en el contexto

                        # Luego renderiza la plantilla pacientes.html con los datos
                        return render(request, 'agendahora.html', {'medicos_data': medicos_data})


                    except Exception as e:
                        # Maneja errores al cargar JSON
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    # Otro error inesperado en la solicitud
                    return HttpResponseServerError()

    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()
    

async def seleccionar_hora(request):

    run = request.POST.get('run')
    print('rut' + run)

    # Realiza una solicitud GET a la URL externa 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'
    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/run-medico/{run}'



    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                if response.status == 200:
                    try:
                        print("hola2")
                        response_json = await response.json()

                        # Procesa los datos recibidos según sea necesario
                        # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                        # Obtener datos específicos del JSON de respuesta
                        agendamedica_data = response_json
                        # Establecer esos datos en el contexto
                        if len(response_json) > 0:
                            # Procesa los datos recibidos según sea necesario
                            # Por ejemplo, podrías extraer datos específicos del JSON de respuesta

                            # Obtener datos específicos del JSON de respuesta
                            agendamedica_data = response_json

                            # Luego renderiza la plantilla agendamedica.html con los datos
                            return render(request, 'seleccionar_hora.html', {'agendamedica_data': agendamedica_data, 'run': agendamedica_data[0]['run_medico']})
                        else:
                            print('no hay datos')
                            print(run)
                            print("hola3")
                            return render(request, 'seleccionar_hora.html', { 'run': str(run)})
                        
                
                    except Exception as e:
                        # Maneja errores al cargar JSON
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    # Otro error inesperado en la solicitud
                    print("hola")
                    return HttpResponseServerError()

    except Exception as e:
        # Maneja errores de solicitud
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()

    


async def confirmar_cita(request):
    if request.method == 'POST':
        print(request)
        run_paciente = request.POST.get('rut_paciente_cita')
        run_medico = request.POST.get('run_medico_cita')
        fecha = request.POST.get('fecha_cita')
        hora_inicio = request.POST.get('hora_inicio_cita')


        

        # Imprimir los datos para depuración
        print(run_paciente),
        print(run_medico),
        print(fecha),
        print(hora_inicio)

        data = {
            'run_paciente': run_paciente,
            'run_medico': run_medico,
            'fecha': fecha,
            'hora_inicio': hora_inicio
        }

        # Configurar encabezados de la solicitud
        headers = {'Content-Type': 'application/json'}

        # Convertir los datos a formato JSON
        json_data = json.dumps(data)

        # Definir la URL del endpoint para la solicitud
        endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/citasmedicas/bloquear-agenda'
        endpoint_url2 = 'https://api.resend.com/emails'

        dataaa = {
    "cc": [],
    "to": ["brayan986788@gmail.com"],
    "bcc": [],
    "from": "onboarding@resend.dev",
    "html": f"<p> <strong>Tu cita para el dia {fecha} a las {hora_inicio} fue agendada con exito</strong>!</p>",
    "tags": [],
    "subject": "Hello World"
}
        json_email = json.dumps(dataaa)
        headers2 = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer re_NdEsLBhj_Fwtzu51jpSRsWdQQZWR4RF7x'
}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint_url, data=json_data, headers=headers) as response:
                    if response.status == 200:
                        async with session.post(endpoint_url2, data=json_email, headers=headers2) as response:
                            print(response)
                        # La solicitud fue exitosa, puedes devolver una JsonResponse con un mensaje de éxito
                        return render(request, 'home.html')
                    else:
                        # La solicitud no fue exitosa, puedes devolver una JsonResponse con un mensaje de error
                        return JsonResponse({'error': 'Error en la solicitud'})
        except Exception as e:
            # Manejar errores de conexión o excepciones, y devolver una JsonResponse con un mensaje de error
            return JsonResponse({'error': str(e)})

    # Si no es una solicitud POST, puedes devolver una JsonResponse con un mensaje de error
    return JsonResponse({'error': 'Solicitud incorrecta'})
