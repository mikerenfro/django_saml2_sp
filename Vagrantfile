# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/rockylinux-8"

  config.vm.hostname = 'django-saml2-auth'
  # config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8443, host: 8443, host_ip: "127.0.0.1"

  config.vm.provision "shell", inline: <<-SHELL
    yum install -y python39-devel python3-virtualenv python39-wheel xmlsec1 xmlsec1-openssl
    yum module enable -y nginx:1.22
    yum install -y nginx
    firewall-cmd --permanent --add-port=8443
    firewall-cmd --reload
    # openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out /etc/pki/tls/certs/localhost.crt -keyout /etc/pki/tls/private/localhost.key
    install -o root -g root -m 0644 /vagrant/localhost.crt /etc/pki/tls/certs/
    install -o root -g root -m 0600 /vagrant/localhost.key /etc/pki/tls/private/
    cp /vagrant/nginx.conf /etc/nginx/
    systemctl enable nginx
    systemctl start nginx
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
    function add_if_missing() {
      grep -qFx "$1" $2 || echo "$1" >> $2
    }
    # Fix project settings
    add_if_missing "INSTALLED_APPS += ['django_extensions']" ${PROJECT}/settings.py
    add_if_missing "INSTALLED_APPS += ['${APP}.apps.${CAP_APP}Config']" ${PROJECT}/settings.py
    add_if_missing 'from .saml2_auth_settings import *' ${PROJECT}/settings.py
    add_if_missing 'SAML2_AUTH = SAML2_AUTH' ${PROJECT}/settings.py

    # Fix project URLs
    add_if_missing 'from django.urls import include' ${PROJECT}/urls.py
    add_if_missing 'from django.views.generic import RedirectView' ${PROJECT}/urls.py
    add_if_missing "urlpatterns += [ path('${APP}/', include('${APP}.urls')), ]" ${PROJECT}/urls.py
    add_if_missing "urlpatterns += [ path('', RedirectView.as_view(url='${APP}/', permanent=True)), ]" ${PROJECT}/urls.py
    add_if_missing 'from django.conf import settings' ${PROJECT}/urls.py
    add_if_missing 'from django.conf.urls.static import static' ${PROJECT}/urls.py
    add_if_missing "urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)" ${PROJECT}/urls.py
    add_if_missing "urlpatterns += [ path('accounts/', include('django.contrib.auth.urls')), ]" ${PROJECT}/urls.py
    add_if_missing "urlpatterns += [ path('saml2_auth/', include('django_saml2_auth.urls')), ]" ${PROJECT}/urls.py
    

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
    echo "Don't forget to add:"
    echo "- the login link to myapp/templates/registration/login.html"
    echo "- the app federation metadata url to saml_sp/saml2_auth_settings.py"
  SHELL
end
