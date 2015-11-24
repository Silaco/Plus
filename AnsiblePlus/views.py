from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import View
from django.shortcuts import render
from django.db import models
import sqlite3

def Login(request):	
	return render(request, 'login.htm')
def AppMaster(request):		
	return render(request, 'ApplicationMaster.html')
def EnvMaster(request):		
	return render(request, 'EnvironmentMaster.html')
def ServerMaster(request):		
	return bindServerMaster(request)
def UserMaster(request):		
	return render(request, 'UserMaster.html')
def index(request):		
	return render(request, 'login.htm')
def home(request):
    return render(request, 'home.html')
def login(request):
	message = 'You submitted an empty form.'	
	if 'user' in request.POST:
		name=request.POST['user']
		pwd=request.POST['pwd']
		
		if name=='testuser' and pwd=='testpwd':
			request.session['access_key'] = name
			request.session.set_expiry(600)
			# return render(request, 'Hosts.htm')
			# return HttpResponse('Welcome :'+name)
			# get(request)			
	return home(request)
def SaveAppMaster(request):
	if 'AppName' in request.POST:
		AppName=request.POST['AppName']
		description=request.POST['AppDesc']
		
		sql = "INSERT INTO tblAppMaster (AppName,AppDesc) VALUES ('"+AppName+"','"+description+"' )"
			
		conn = sqlite3.connect('ansible.db')
		
		conn.execute(sql);
		conn.commit();
		message = 'Application Name : '+AppName
	else:
		message = 'You submitted an empty form.'
	return home(request)
def SaveEnvMaster(request):
	if 'envName' in request.POST:
		envName=request.POST['envName']
		description=request.POST['envDesc']
		
		sql = "INSERT INTO tblEnvMaster (EnvName,EnvDesc) VALUES ('"+envName+"','"+description+"' )"
			
		conn = sqlite3.connect('ansible.db')
		
		conn.execute(sql);
		conn.commit();
		message = 'Environment Name : '+envName
	else:
		message = 'You submitted an empty form.'
	return home(request)
def SaveUserMaster(request):
	if 'UserName' in request.POST:
		UserName=request.POST['UserName']
		UserEmail=request.POST['UserEmail']
		userEID=request.POST['userEID']
		
		sql = "INSERT INTO tblUserMaster (Name,Email,UserEID) VALUES ('"+UserName+"','"+UserEmail+"','"+userEID+"'  )"
			
		conn = sqlite3.connect('ansible.db')
		
		conn.execute(sql);
		conn.commit();
		message = 'User Name : '+UserName
	else:
		message = 'You submitted an empty form.'
	return home(request)
def SaveServerMaster(request):
	if 'serverip' in request.GET:
		Serverip=request.GET['serverip']
		serverhost=request.GET['serverhost']
		serveruser=request.GET['serveruser']
		serverpwd=request.GET['serverpwd']
		App=request.GET['App']
		Env=request.GET['Env']
		
		sql = "INSERT INTO tblServerMaster (ServerIP,ServerHost,ServerUserName,ServerCredential,Env,Application) VALUES ('"+Serverip+"','"+serverhost+"','"+serveruser+"','"+serverpwd+"','"+Env+"','"+App+"')"
			
		conn = sqlite3.connect('ansible.db')
		
		conn.execute(sql);
		conn.commit();
		message = 'Server IP: '+Serverip
	else:
		message = 'You submitted an empty form.'
	return home(request)
def SaveTemplateMaster(request):
	if 'Temp' in request.POST:
		Temp=request.POST['Temp']
		TempName=request.POST['TempName']
		TempGitUrl=request.POST['TempGitUrl']
		playbooks=request.POST['playbooks']
		
		sql = "INSERT INTO tblTemplateMaster (Template,TempNa,TempGitUrl,PlayBook) VALUES ('"+Temp+"','"+TempName+"','"+TempGitUrl+"','"+playbooks+"')"
			
		conn = sqlite3.connect('ansible.db')
		
		conn.execute(sql);
		conn.commit();
		message = 'Teamplate Name: '+Temp
	else:
		message = 'You submitted an empty form.'
	return home(request)
def TemplateMaster(request):
    return render(request, 'TemplateMaster.html')
    
def SetupPlay(request):
    import ansiblepythonapi as myPlay
    args=['test.yml']
    message=myPlay.main(args)
    html=''
    html+='<table border=1 cellspacing=5 cellpadding=5>'
    
    for runner_results in myPlay.message:      
        # message.append(runner_results)
        for (host, value) in runner_results.get('dark', {}).iteritems():
            html+='<tr>'            
            html+='<td>'+host+'</td>'
            html+='<td>'+str(value['failed'])+'</td>'
            html+='<td>'+str(value['msg'])+'</td>'
            html+='</tr>'    
        for (host, value) in runner_results.get('contacted', {}).iteritems():
            html+='<tr>'            
            html+='<td>'+host+'</td>'
            html+='<td>'+str(value['failed'])+'</td>'
            html+='<td>'+str(value['msg'])+'</td>'
            html+='</tr>'
        # for msg in pb.stats.output():               
        # print msg
    html+='</table>'
    return HttpResponse(html)
def Play(request):
    return bindPlay(request)
    #return render(request, 'Play.html')
def bindTemplateMaster(request):
	try:
		key = request.session['access_key']
		age = request.session.get_expiry_age()
		if age > 10:
			index(request)
	except:
		Login(request)		 
	conn = sqlite3.connect('ansible.db')
	Apps = conn.execute("SELECT DISTINCT AppName from tblAppMaster")
	App = []
	for row in Apps:
		App.append(str(row[0]))
	Envs = conn.execute("SELECT DISTINCT EnvName from tblEnvMaster")
	Env = []
	for row in Envs:
		Env.append(str(row[0]))    
	conn.close()			
	context=Context({'App':App,'Env':Env})
	return render(request, 'play.html',context)
def bindServerMaster(request):
	try:
		conn = sqlite3.connect('ansible.db')
		Apps = conn.execute("SELECT DISTINCT AppName from tblAppMaster")
		App = []
		for row in Apps:
			App.append(str(row[0]))
		Envs = conn.execute("SELECT DISTINCT EnvName from tblEnvMaster")
		Env = []
		for row in Envs:
			Env.append(str(row[0]))    
		conn.close()			
		context=Context({'App':App,'Env':Env})
		return render(request, 'ServerMaster.html',context)
	except:
		Login(request)		 
	
def SubmitPlay(request):	
    import jinja2
    from tempfile import NamedTemporaryFile
    import os

   
    html = ''

    inventory = """
    [current]
    {{ public_ip_address }}
    """
    for row in request.GET:
        if row.name=='Servers':
            html=html+str(row.value+'\n')
   


    inventory_template = jinja2.Template(inventory)
    rendered_inventory = inventory_template.render({
        'public_ip_address': html    
        # and the rest of our variables
    })

    # Create a temporary file and write the template string to it
    hosts = NamedTemporaryFile(delete=False)
    hosts.write(rendered_inventory)
    hosts.close()

    import ansiblepythonapi as myPlay
    args=['test.yml']
    args.append('-i')
    args.append(host.name)
    message=myPlay.main(args)

    objects=[]
    for runner_results in myPlay.message:              
        values=[]
        for (host, value) in runner_results.get('dark', {}).iteritems():
            values.append(host)
            values.append(value['failed'])
            values.append(value['msg'])    
            objects.append(values)
        for (host, value) in runner_results.get('contacted', {}).iteritems():
            values.append(host)
            values.append(value['failed'])
            values.append(value['msg'])    
            objects.append(values)
        # for msg in pb.stats.output():   
    context=Context({'Summary':objects})
    return render(request, 'AnsibleResponce.html',context)
def Mapping(request):
    return bindMapping(request)
def bindMapping(request):
	try:
		conn = sqlite3.connect('ansible.db')
		Apps = conn.execute("SELECT DISTINCT AppName from tblAppMaster")
		App = []
		for row in Apps:
			App.append(str(row[0]))
		Envs = conn.execute("SELECT DISTINCT EnvName from tblEnvMaster")
		Env = []
		for row in Envs:
			Env.append(str(row[0]))
		Users = conn.execute("SELECT DISTINCT Name from tblUserMaster")
		User = []
		for row in Users:
			User.append(str(row[0]))
		Hosts = conn.execute("SELECT DISTINCT ServerHost from tblServerMaster")
		Host = []
		for row in Hosts:
			Host.append(str(row[0]))
		conn.close()			
		context=Context({'App':App,'Env':Env,'User':User,'Host':Host})
		return render(request, 'Mapping.html',context)
	except:
		Login(request)
def SaveMappings(request):
	if 'App' in request.GET:
		App=request.GET['App']
		Env=request.GET['Env']
		User=request.GET['User']
		Host=request.GET['Host']
				
		sql = "INSERT INTO tblMapping (App,Env,User,HostName) VALUES ('"+App+"','"+Env+"','"+User+"','"+Host+"')"
			
		conn = sqlite3.connect('ansible.db')
		
		conn.execute(sql);
		conn.commit();
		message = 'Application: '+App
	else:
		message = 'You submitted an empty form.'
	return home(request)
def Contacts(request):
	return render(request,'contact.html')
def bindPlay(request):
	try:
		key = request.session['access_key']
		age = request.session.get_expiry_age()
		if age > 10:
			index(request)
	except:
		Login(request)		 
	conn = sqlite3.connect('ansible.db')
	Apps = conn.execute("SELECT DISTINCT AppName from tblAppMaster")
	App = []
	for row in Apps:
		App.append(str(row[0]))
	Envs = conn.execute("SELECT DISTINCT EnvName from tblEnvMaster")
	Env = []
	for row in Envs:
		Env.append(str(row[0]))
	Servers = conn.execute("SELECT DISTINCT serverhost from tblServerMaster")
	Server = []
	for row in Servers:
		Server.append(str(row[0]))
	Temps = conn.execute("SELECT DISTINCT Template from tblTemplateMaster")
	Temp = []
	for row in Temps:
		Temp.append(str(row[0]))
	conn.close()			
	context=Context({'App':App,'Env':Env,'Server':Server,'Temp':Temp})
	return render(request, 'play.html',context)
	

			
