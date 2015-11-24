from django.conf.urls import include, url
from AnsiblePlus.views import index,AppMaster,EnvMaster,ServerMaster,UserMaster,login,Login,SaveAppMaster,SaveEnvMaster,SaveUserMaster,SaveServerMaster,home,SaveTemplateMaster,TemplateMaster,Play,bindTemplateMaster,SubmitPlay,Mapping,SetupPlay

urlpatterns = [
	url(r'^login/$',login,name='login'),
	url(r'^Login/$',Login,name='Login'),
	url(r'^index/$',index,name='index'),
	url(r'^AppMaster/$',AppMaster,name='AppMaster'),
	url(r'^EnvMaster/$',EnvMaster,name='EnvMaster'),
	url(r'^ServerMaster/$',ServerMaster,name='ServerMaster'),
	url(r'^UserMaster/$',UserMaster,name='UserMaster'),
	url(r'^SaveAppMaster/$',SaveAppMaster,name='SaveAppMaster'),
	url(r'^SaveEnvMaster/$',SaveEnvMaster, name='SaveEnvMaster'),
	url(r'^SaveUserMaster/$',SaveUserMaster, name='SaveUserMaster'),
	url(r'^SaveServerMaster/$',SaveServerMaster, name='SaveServerMaster'),
	url(r'^home/$',home, name='home'),
    url(r'^SaveTemplateMaster/$',SaveTemplateMaster, name='SaveTemplateMaster'),
    url(r'^TemplateMaster/$',TemplateMaster, name='TemplateMaster'),
    url(r'^Play/$',Play, name='Play'),
    url(r'^bindTemplateMaster/$',bindTemplateMaster, name='bindTemplateMaster'),
    url(r'^SubmitPlay/$',SubmitPlay, name='SubmitPlay'),
	# url(r'^Mapping/$',Mapping, name='Mapping'),
    url(r'^SetupPlay/$',SetupPlay, name='SetupPlay')    
]