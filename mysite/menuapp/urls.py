from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
import menuapp.views


urlpatterns = [
    # Examples:
    # url(r'^$', 'factura.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', menuapp.views.index_menu),
    #url(r'^/$',  'menuapp.views.index_menu'),
    url(r'^add/$', menuapp.views.add_menu),
    url(r'^edit/(?P<pk>\d+)$', menuapp.views.edit_menu),
    url(r'^delete/(?P<pk>\d+)$', menuapp.views.delete_menu),
    url(r'^get_menu_items/$', menuapp.views.get_menu_items),
    

]