#from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404,render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse  , HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.contrib.auth import authenticate, login, logout
from comunes import *
from models import *
from forms import *



def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, ('Ha salido con exito'))
    return HttpResponseRedirect('/')

def login_user(request):    
    error=""
    msg=""
    # if request.GET.get('next'):
    #   return HttpResponseRedirect(next)
    # else:
    if request.GET:
        next = request.GET['next']

    if request.POST:
        username = request.POST['username']
        password = request.POST['password'] 
        next = request.POST.get('next')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                #messages.add_message(request, messages.SUCCESS, ('Se ha logueado correctamente!'))
                if next:
                    #request=register_sessions(request)
                    return HttpResponseRedirect(next)
                else:                            
                    return HttpResponseRedirect('/')                            
            else:
                msg="El usuario esta inactivo"
                #messages.add_message(request, messages.ERROR, ('No se pudo loguear'))
        else:
            msg="usuario no existe"             
            error="No se pudo loguear, %s" % msg

    form = MyLoginForm()    

    
        # if  next == "/":
        #   pass
        # else:
        #   error="No tiene permisos para esta funcionalidad"
        
    return render(request,'menuapp/login.html', {'form':form, 'error':error,'next':next})


@login_required(login_url='/login/')
def main(request):
    #valido si la empresa esta creada, debe estarlo

    mensaje=[]
    #_count=Empresa.objects.count()
    
    # if _count==0:
    #     mensaje.append("No ha configurado su empresa. Vaya a Opciones->Configurar Empresa") 
    # elif _count>1:
    #     mensaje.append("Error de configuracion de empresa")
    # else:
    #     empresa=Empresa.objects.all()[:1]
    #     empresa=empresa[0]
    #     request.session['empresa'] = {'razon_social':empresa.razon_social,'rif':empresa.rif,
    #                             'logo':empresa.ruta_foto.url,'nit':empresa.nit,'tlf':empresa.tlf,
    #                             'fax':empresa.fax,'email':empresa.email,'direccion':empresa.direccion,
    #                             'p1':empresa.p1,'p2':empresa.p2,'p3':empresa.p3,'p4':empresa.p4,
    #                             'p5':empresa.p5,'ancho_logo':empresa.ancho_logo, 'alto_logo':empresa.alto_logo,
    #                             'show_logo':empresa.show_logo
    #                                 }
      
    
    # try:
    #     impuesto=TipoImpuesto.objects.get(codigo='G')
    # except TipoImpuesto.DoesNotExist:
    #     mensaje.append("Necesita configurar el impuesto Al menos uno debe tener codigo G. Click en Configurar->Tipo de Impuestos")
    # else:
    #     request.session['impuesto'] = {'G':str(impuesto.valor)}
    #print request.session['impuesto']['G']
    #
    
    return render(request, 'menuapp/index.html', {
            'mensaje': mensaje,            
        })

def register_sessions(request):
    mensaje=[]
    _count=Empresa.objects.count()
    
    if _count==0:
        mensaje.append("No ha configurado su empresa. Vaya a Opciones->Configurar Empresa") 
    elif _count>1:
        mensaje.append("Error de configuracion de empresa")
    else:
        empresa=Empresa.objects.all()[:1]
        empresa=empresa[0]
        request.session['empresa'] = {'razon_social':empresa.razon_social,'rif':empresa.rif,
                                'logo':empresa.ruta_foto.url,'nit':empresa.nit,'tlf':empresa.tlf,
                                'fax':empresa.fax,'email':empresa.email,'direccion':empresa.direccion,
                                'p1':empresa.p1,'p2':empresa.p2,'p3':empresa.p3,'p4':empresa.p4,
                                'p5':empresa.p5,'ancho_logo':empresa.ancho_logo, 'alto_logo':empresa.alto_logo,
                                'show_logo':empresa.show_logo

                                    }
        # return HttpResponseRedirect('/empresa/')
    
    try:
        impuesto=TipoImpuesto.objects.get(codigo='G')
    except TipoImpuesto.DoesNotExist:
        mensaje.append("Necesita configurar el impuesto Al menos uno debe tener codigo G. Click en Configurar->Tipo de Impuestos")
    else:
        request.session['impuesto'] = {'G':str(impuesto.valor)}
    #print request.session['impuesto']['G']
    #
    return request

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            print "error salvando"

    #args = {}
    #args.update(csrf(request))
    form = MyRegistrationForm()
    #print args
    return render(request, 'register.html', {'form':form})  


def get_menu_items(request):
    submenu=request.GET.get('submenu',None)
    #print submenu
    if not submenu:
        menu_items = MenuItem.objects.filter(parent__codigo=None)
        # string en blanco no back button
        back_button=''
    else:
        menu_items = MenuItem.objects.filter(parent__codigo=submenu)
        #string con back button
        back_button=""" 
         <div class=\"col-xs-3 col-sm-3 col-md-3 \" id=\"menu-items\">  \
        <a href=\"%s\" class=\"thumbnail\" onclick=\"%s\"> \
        <img src='/media/%s' title = '%s' class='img-responsive' > \
        </a> \
        <div class='post-content-menu'>\
        <p>%s</p>\
        </div>\
        </div> """ % ("javascript:void(0)", "get_menu_items() ","icons/back.png","Vuelve al menu anterior","Volver")
    
    cat = ""
    for element in menu_items:
        cat+= "<div class=\"col-xs-3 col-sm-3 col-md-3 \" id=\"menu-items\">  \
        <a href=\"%s\" class=\"thumbnail\" onclick=\"%s\"> \
        <img src='/media/%s' title = '%s' class='img-responsive' > \
        </a> \
        <div class='post-content-menu'>\
        <p>%s</p>\
        </div>\
        </div> " % (element.url,element.onclick,element.ruta_foto,element.descripcion,element.nombre)

    cat+= back_button
    return HttpResponse(cat)


@login_required(login_url='/login/')
#@user_passes_test(is_in_menu_group, login_url='/login/')
def index_menu(request):
    form_class = GenericSearchForm
    model = MenuItem
    template_name = 'menuapp/index_menu.html'
    paginate_by = 10

    form = form_class(request.POST or None)
    if form.is_valid():
        menu_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
    else:
        menu_list = model.objects.all()

    paginator = Paginator(menu_list, paginate_by) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'menus': menus,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
#@permission_required('menuapp.add_menuitem', login_url='/login/')
def add_menu(request):
    template_name="menuapp/menu.html"
    if request.method == 'POST':
        form = ManageMenuItems(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/menuapp/')
    else:
        form = ManageMenuItems()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
#@permission_required('menuapp.change_menuitem', login_url='/login/')
def edit_menu(request,pk):
    menu = get_object_or_404(MenuItem, pk=pk)        
    form = ManageMenuItems(instance=menu)    
    #print form.nombres
    if request.POST:
        form = ManageMenuItems(request.POST,request.FILES,instance=menu)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/menuapp/')        

    return render_to_response('menuapp/menu.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
#@permission_required('menuapp.delete_menuitem', login_url='/login/')
def delete_menu(request,pk):
	menu = get_object_or_404(MenuItem, pk=pk)        
	form = ManageMenuItems(instance=menu)    
    #print form.nombres
	if request.POST:
		form = ManageMenuItems(request.POST,request.FILES,instance=menu)    
		if form.is_valid():
			menu.delete()            
			messages.add_message(request, messages.SUCCESS, ('menu eliminada'))
			return HttpResponseRedirect('/menuapp/')        

	return render_to_response('menuapp/menu.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))