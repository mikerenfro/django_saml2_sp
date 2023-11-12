# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/rockylinux-8"

  config.vm.hostname = 'django-saml2-auth'
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"

  config.vm.provision "shell", inline: <<-SHELL
    yum install -y python39-devel python3-virtualenv python39-wheel xmlsec1 xmlsec1-openssl
  SHELL
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    python3.9 -m venv ~/venv
    source ~/venv/bin/activate
    pip install Django==3.2.20 django_saml2_auth django-extensions
    cd /vagrant
    PROJECT=saml_sp
    CAP_APP=Myapp
    APP=$(echo ${CAP_APP} | tr '[A-Z]' '[a-z]') # Myapp -> myapp
    if [ ! -d ${PROJECT} ]; then
      echo "Creating Django project ${PROJECT}"
      django-admin startproject ${PROJECT}
    else
      echo "Django project ${PROJECT} already created"
    fi
    cd ${PROJECT}
    if [ ! -d ${APP} ]; then
      echo "Creating Django app ${APP}"
      python manage.py startapp ${APP}
    else
      echo "Django app ${APP} already created"
    fi
    # Fix project settings
    grep -qF "INSTALLED_APPS += ['django_extensions']" ${PROJECT}/settings.py || echo "INSTALLED_APPS += ['django_extensions']" >> ${PROJECT}/settings.py
    grep -qF "INSTALLED_APPS += ['${APP}.apps.${CAP_APP}Config']" ${PROJECT}/settings.py || echo "INSTALLED_APPS += ['${APP}.apps.${CAP_APP}Config']" >> ${PROJECT}/settings.py
    grep -qF 'from .saml2_auth_settings import *' ${PROJECT}/settings.py || echo 'from .saml2_auth_settings import *' >> ${PROJECT}/settings.py
    grep -qF 'SAML2_AUTH = SAML2_AUTH' ${PROJECT}/settings.py || echo 'SAML2_AUTH = SAML2_AUTH' >> ${PROJECT}/settings.py

    # Fix project URLs
    grep -qF '^from django.urls import include' ${PROJECT}/urls.py || echo "from django.urls import include" >> ${PROJECT}/urls.py
    grep -qF '^from django.views.generic import RedirectView' ${PROJECT}/urls.py || echo "from django.views.generic import RedirectView" >> ${PROJECT}/urls.py
    grep -qF "urlpatterns += [ path('${APP}/', include('${APP}.urls')), ]" ${PROJECT}/urls.py || echo "urlpatterns += [ path('${APP}/', include('${APP}.urls')), ]" >> ${PROJECT}/urls.py
    grep -qF "urlpatterns += [ path('', RedirectView.as_view(url='${APP}/', permanent=True)), ]" ${PROJECT}/urls.py || echo "urlpatterns += [ path('', RedirectView.as_view(url='${APP}/', permanent=True)), ]" >> ${PROJECT}/urls.py
    grep -qF '^from django.conf import settings' ${PROJECT}/urls.py || echo "from django.conf import settings" >> ${PROJECT}/urls.py
    grep -qF '^from django.conf.urls.static import static' ${PROJECT}/urls.py || echo "from django.conf.urls.static import static" >> ${PROJECT}/urls.py
    grep -qF 'urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)' ${PROJECT}/urls.py || echo "urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)" >> ${PROJECT}/urls.py
    grep -qF "accounts/" ${PROJECT}/urls.py || echo "urlpatterns += [ path('accounts/', include('django.contrib.auth.urls')), ]" >> ${PROJECT}/urls.py
    grep -qF "urlpatterns += [ path('saml2_auth/', include('django_saml2_auth.urls')), ]" ${PROJECT}/urls.py || echo "urlpatterns += [ path('saml2_auth/', include('django_saml2_auth.urls')), ]" >> ${PROJECT}/urls.py
    

    # Fix project scripts
    cp -a ../project_py/* ${PROJECT}

    # Fix app templates, scripts, static content
    cp -a ../app_templates ${APP}/templates
    cp -a ../app_py/* ${APP}/
    mkdir -p ${APP}/static ; cp -a ../app_static/* ${APP}/static/
    # Get ready to run
    python manage.py makemigrations
    python manage.py migrate
    # Create superuser and regular user
    mkdir -p scripts
    cp ../auto_create_users.py scripts
    python manage.py runscript auto_create_users
    # python manage.py runserver 0.0.0.0:8000
  SHELL
end
