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
			
		conn = sqlite3.connect('C:/Users/v480618/rama.db')
		
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
			
		conn = sqlite3.connect('C:/Users/v480618/rama.db')
		
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
			
		conn = sqlite3.connect('C:/Users/v480618/rama.db')
		
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
			
		conn = sqlite3.connect('C:/Users/v480618/rama.db')
		
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
		
		sql = "INSERT INTO tblTemplateMaster (Template,TempName,TempGitUrl,PlayBook) VALUES ('"+Temp+"','"+TempName+"','"+TempGitUrl+"','"+playbooks+"')"
			
		conn = sqlite3.connect('C:/Users/v480618/rama.db')
		
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
    html+='<table>'
    
    for runner_results in myPlay.message:      
        # message.append(runner_results)
        for (host, value) in runner_results.get('dark', {}).iteritems():
            html+='<tr>'            
            html+='<td>'+host+'</td>'
            html+='<td>'+value+'</td>'
            html+='</tr>'    
        for (host, value) in runner_results.get('contacted', {}).iteritems():
            html+='<tr>'            
            html+='<td>'+host+'</td>'
            html+='<td>'+value+'</td>'
            html+='</tr>'
        # for msg in pb.stats.output():               
        # print msg
    html+='</table>'
    return HttpResponse(html)
def Play(request):
    return bindTemplateMaster(request)
    #return render(request, 'Play.html')
def bindTemplateMaster(request):
	try:
		key = request.session['access_key']
		age = request.session.get_expiry_age()
		if age > 10:
			index(request)
	except:
		Login(request)		 
	conn = sqlite3.connect('C:/Users/v480618/rama.db')
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
		conn = sqlite3.connect('C:/Users/v480618/rama.db')
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
    return render(request, 'TemplateMaster.html')	
	

			
