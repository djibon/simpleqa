from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
   (r'^admin/', include(admin.site.urls)),
   url(r'^accounts/login/$', 'django.contrib.auth.views.login',name='account-login'),
   url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'},name='account-logout'),
   (r'', include('core.urls')),
)
