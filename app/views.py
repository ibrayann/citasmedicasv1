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
                            
                            return JsonResponse(response_json, status=200)
                        except Exception as e:
   
                            print(f"Error al cargar JSON: {e}")
                            return HttpResponseServerError()
                    elif response.status == 404:
 
                        return JsonResponse({'message': 'Usuario no registrado'}, status=404)
                    elif response.status == 401:

                        return JsonResponse({'message': 'Credenciales inválidas'}, status=401)
                    else:
  
                        return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
        except Exception as e:

            print(f"Error en la solicitud: {e}")
            return HttpResponseServerError()


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
                            
                            return JsonResponse(response_json, status=201)
                        except Exception as e:
                            print(f"Error al cargar JSON: {e}")
                            return HttpResponseServerError()
                    elif response.status == 500:
                        return JsonResponse({'message': 'Usuario no registrado, verifique email o rut no esten asociados a una cuenta'}, status=404)
                    else:
                        return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
                    
        except Exception as e:
            print(f"Error en la solicitud: {e}")
            return HttpResponseServerError()

    return render(request, 'register.html')

async def pacientes(request):
    endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/pacientes'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        print(response_json)

                        pacientes_data = response_json

                        return render(request, 'pacientes.html', {'pacientes_data': pacientes_data})


                    except Exception as e:
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    return HttpResponseServerError()

    except Exception as e:

        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()


def home(request):
    return render(request, 'home.html')

def logout(request):
    return render(request, 'logout.html')

async def medicos(request):
    endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/medicos'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        medicos_data = response_json

                        return render(request, 'medicos.html', {'medicos_data': medicos_data})


                    except Exception as e:
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    return HttpResponseServerError()

    except Exception as e:
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()

async def agendamedica(request, run):
    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/run-medico/{run}'


    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                if response.status == 200:
                    try:
                        response_json = await response.json()


                        agendamedica_data = response_json
                        if len(response_json) > 0:
                            
                            agendamedica_data = response_json

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
                    return []

    except Exception as e:
        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()


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
                            
                            
                            return JsonResponse(response_json, status=201)
                        except Exception as e:
                            print(f"Error al cargar JSON: {e}")
                            return HttpResponseServerError()
                    elif response.status == 500:
                        return JsonResponse({'message': 'Usuario no registrado, verifique email o rut no esten asociados a una cuenta'}, status=404)
                    else:
                        return JsonResponse({'error': f'Error {response.status} en la solicitud a {endpoint_url}'}, status=500)
                    
        except Exception as e:
            print(f"Error en la solicitud: {e}")
            return HttpResponseServerError()

    return render(request, 'registermedico.html')

async def citas_medicas(request):
    endpoint_url = 'https://controlcitasmedicas.brayan986788.repl.co/api/citasmedicas/'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        citas_data = response_json

                        return render(request, 'citas.html', {'citas_data': citas_data})


                    except Exception as e:
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:
                    return HttpResponseServerError()

    except Exception as e:
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
    
def enviar_correo(request):
    if request.method == 'POST':

        destinatario = request.POST['destinatario']
        asunto = request.POST['asunto']
        contenido = request.POST['contenido']

        api_key = 'TU_CLAVE_DE_API'

        # Crea un objeto Mail
        message = Mail(
            from_email='tucorreo@gmail.com',
            to_emails=destinatario,
            subject=asunto,
            plain_text_content=contenido)

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            if response.status_code == 202:
                return render(request, 'correo_enviado.html')
            else:
                return render(request, 'error_envio_correo.html')

        except Exception as e:
            return render(request, 'error_envio_correo.html')

    return render(request, 'formulario_correo.html')


async def formulario_cita(request):
    return  render(request,'formulario_cita.html')
    

async def agendarhora(request):
    sucursal = request.GET.get('sucursal')
    especialidad = request.GET.get('especialidad')

    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/medicos/medicos_sucursal_especialidad/{sucursal}/{especialidad}'
    print(sucursal)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                print(response.status)
                
                if response.status == 200:
                    try:
                        response_json = await response.json()

                        medicos_data = response_json
                        print(medicos_data)

                        return render(request, 'agendahora.html', {'medicos_data': medicos_data})


                    except Exception as e:
   
                        print(f"Error al cargar JSON: {e}")
                        return HttpResponseServerError()
                else:

                    return HttpResponseServerError()

    except Exception as e:

        print(f"Error en la solicitud: {e}")
        return HttpResponseServerError()
    

async def seleccionar_hora(request):

    run = request.POST.get('run')
    print('rut' + run)


    endpoint_url = f'https://controlcitasmedicas.brayan986788.repl.co/api/agendamedica/run-medico/{run}'



    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint_url) as response:
                if response.status == 200:
                    try:
                        print("hola2")
                        response_json = await response.json()
                        agendamedica_data = response_json

                        if len(response_json) > 0:

                            agendamedica_data = response_json

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

        headers = {'Content-Type': 'application/json'}

        json_data = json.dumps(data)
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
               
                        return render(request, 'home.html')
                    else:

                        return JsonResponse({'error': 'Error en la solicitud'})
        except Exception as e:
   
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Solicitud incorrecta'})
