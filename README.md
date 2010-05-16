Django Learning Project
=======================

<p>Getting Apache ready for serving Python applications seems to really be a headache. <code>mod_python</code> seems relatively easy, but the preferred <code>mod_wsgi</code> seems to give everyone headaches. I wanted to serve my python applications using MAMP since it's part of my daily workflow. I found a decent solution that is working really well for me with MAMP on OSX (Leopard). You may want to check out my previous post on <a href="http://typeoneerror.com/blog/post/django-stack-install-activepython-win-mac" title="Typeoneerror / Blog">installing and managing a basic OSX Django Stack</a> before reading this one.</p>

<h3>Installing WSGI</h3>

<p>To install WSGI, you need to compile it against the version of Apache you'll be using it with. MAMP's current packaged version of Apache is 2.0.63, which is not <em>super</em> new, but will do. If you're like me and you just installed the MAMP binary instead of downloading the source code...well, then you don't have the Apache source code for 2.0.63, do you? So, let's get it!</p>

<p>I had already <a href="http://www.macports.org/install.php" title="The MacPorts Project -- Download &amp; Installation">installed Macports</a> in my previous adventure with Django installs. I decided to see what was available Apache-wise, and lo-and-behold:

<pre>
$ port search "apache"
apache20 @2.0.63 (www)
    The extremely popular second version of the Apache http server</pre>
    
<p>The exact same version that MAMP is packaged with! Awesome! Let's install it...</p>

<pre>
$ port install apache20</pre>

<p>That'll install Apache in <em>/opt/local/apache20</em> (or wherever Macports is installing stuff on your machine). Next you'll need to <a href="http://code.google.com/p/modwsgi/downloads/list" title="Downloads - modwsgi - Project Hosting on Google Code">grab the mod_wsgi source</a> from author Graham Dumpleton (thanks, Graham!). Unpack that tar.gz file and fire up terminal and cd into that folder. First read this code section:

<pre>
mod_wsgi-3.2 $ ./configure

checking for apxs2... no
checking for apxs... /usr/sbin/apxs
checking Apache version... 2.2.14
checking for python... /Library/Frameworks/Python.framework/Versions/2.6/bin/python
configure: creating ./config.status
config.status: creating Makefile</pre>

<p>So our basic configure checks for apxs (apache extension tool) and finds the default OSX install ‚Äì which for me is currently 2.2.14; too new for MAMP. So go ahead and add the --with-apxs flag to the configure and point to wherever Macports installed your apache20:</p>

<pre>
mod_wsgi-3.2 $ ./configure --with-apxs=/opt/local/apache20/bin/apxs
checking Apache version... 2.0.63
checking for python... /Library/Frameworks/Python.framework/Versions/2.6/bin/python
configure: creating ./config.status
config.status: creating Makefile</pre>

<p>Ok, so the Apache version looks right this time. Let's make and install that guy:</p>

<pre>
$ make
$ sudo make install
chmod 755 /opt/local/apache20/modules/mod_wsgi.so</pre>

<p>Cool, so looks like it copied the compiled wsgi module into our apache20 installation. Now we just need to copy it to <em>/Applications/MAMP/Library/modules</em> (your MAMP modules folder).</p>

<p>Fire up MAMP Pro and go to <em>File > Edit Template > Apache httpd.conf</em>. Add the following after the other LoadModule directives:</p>

<pre>
LoadModule wsgi_module modules/mod_wsgi.so</pre>

<p>Ok, that's the install. Stop and start MAMP services and you've got WSGI ready to serve python apps. Next step is to configure a Django site to be served.</p>

<h3>Using WSGI</h3>

<p>To start, I've <a href="http://github.com/typeoneerror/django-learning/tree/master/project/" title="project at master from typeoneerror's django-learning - GitHub">commited my "learning" code to github</a>, so you can check out how I'm learning how to set up and use Django on my machine. I'll be referencing these files throughout so grab them if you want them. I'm also assuming you've created a basic Django project and an application. My learning code uses the same code from the introduction tutorial on the djangoproject.com site. My sample code is in a directory called "project" and I have an application called "polls."</p>

<p>First thing you want to do is create a named host like you always do with MAMP. Switch to the hosts panel and hit the "+" button. I called this one "django.dev". In the General settings, point the document root to your project's root; in my case it points to <em>/Library/WebServer/Documents/Django/project</em>.</p>

<p>Now in your django project, create a folder called "apache" and create two files there.</p>

<pre>
/project/
    /apache/
        apache_django_wsgi.conf
        django.wsgi
    settings.py
    polls
    ...</pre>
    
<p>See the two files and folder stucture on github <a href="http://github.com/typeoneerror/django-learning/tree/master/project/apache" title="project/apache at master from typeoneerror's django-learning - GitHub">here</a>. django.wsgi is your primary wsgi application. This is mounted as the root of your website:</p>

<pre>
import os, sys

# path to parent folder of project
sys.path.append('/Library/Webserver/Documents/Django')
# path to your settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

# create a wsgi "application"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()</pre>

You can see my setup <a href="http://github.com/typeoneerror/django-learning/blob/master/project/apache/django.wsgi" title="project/apache/django.wsgi at master from typeoneerror's django-learning - GitHub">here</a>. apache_django_wsgi.conf is the httpd.conf file for your VirtualHost:

<pre>
Alias /static /Library/Webserver/Documents/Django/project/static

&lt;Directory /Library/Webserver/Documents/Django/project/media&gt;
Order deny,allow
Allow from all
&lt;/Directory&gt;

WSGIScriptAlias / /Library/Webserver/Documents/Django/project/apache/django.wsgi</pre>

<p>You can see that <a href="http://github.com/typeoneerror/django-learning/blob/master/project/apache/apache_django_wsgi.conf" title="project/apache/apache_django_wsgi.conf at master from typeoneerror's django-learning - GitHub">mine</a> defines an alias that points to a static folder (where I'll serve my js, css, images from for now) and a <code>WSGIScriptAlias</code> which is the full path to my .wsgi application.</p>

<p>Now back in MAMP, go to the advanced settings of your virtual host and in the "Customized virtual host general settings" add:</p>

<pre>
Include /Library/Webserver/Documents/Django/project/apache/apache_django_wsgi.conf</pre>

<p>This would be the full path to your .conf file in your project. Again, restart MAMP's services. So now when you hit django.dev, the application defined in your .wsgi will be served. django.dev/static/ will be avaiable for you to add static content like js, css, etc. The end.</p>
