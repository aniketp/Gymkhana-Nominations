from django.apps import AppConfig


class NomiConfig(AppConfig):
    name = 'nomi'



"""
class ncnvjk=fnvkjdfvlkk
fdvnkGET and POST are the only HTTP methods to use when dealing with forms.

Django’s login form is returned using the POST method, in which the browser 
 up the form data, encodes it for transmission, sends it to the server, and then
  receives back its response.

GET, by contrast, bundles the submitted data into a string, and uses this to compose 
a URL. The URL contains the address where the data must be sent, as well as the data k
eys and values. You can see this in action if you do a search in the Django documentation, which 
will produce a URL of the form https://docs.djangoproject.com/search/?q=forms&release=1.


GET and POST are typically used for different purposes.

Any request that could be used to change the state of the system - for example, a request 
that makes changes in the database - should use POST. GET should be used only for requests
 that do not affect the state of the system.

GET would also be unsuitable for a password form, because the password would appear in the URL, 
and thus, also in browser history and server logs, all in plain text. Neither would it be suitable 
for large quantities of data, or for binary data, such as an image. A Web application that uses GET requests for admin forms is a security risk: it can be easy for an attacker to mimic a form’s request to gain access to sensitive parts of the system. POST, coupled with other protections like Django’s CSRF protection offers more control over access.

On the other hand, GET is suitable for things like a web search form, because the URLs that represent a GET request can easily be bookmarked, shared, or resubmitted.
Django’s role in forms¶

Handling forms is a complex business. Consider Django’s admin, where numerous items of data o
f several different types may need to be prepared for display in a form, rendered as HTML, edited 
using a convenient interface, returned to the server, validated and cleaned up, and then saved or 
passed on for further processing.

Django’s form functionality can simplify and automate vast portions of this work, and can 
also do it more securely than most programmers would be able to do in code they wrote themselves.

Django handles three distinct parts of the work involved in forms:

    preparing and restructuring data to make it ready for rendering
    creating HTML forms for the data
    receiving and processing submitted forms and data from the client

It is possible to write code that does all of this manually, but Django can take care of it
 all for you.
Forms in Django¶

We’ve described HTML forms briefly, but an HTML <form> is just one part of the machinery required.

In the context of a Web application, ‘form’ might refer to that HTML <form>, or to the Django Form that produces it, or to the structured data returned when it is submitted, or to the end-to-end working collection of these parts.
The Django Form class¶

At the heart of this system of components is Django’s Form class. In much the same way that a Django model describes the logical structure of an object, its behavior, and the way its parts are represented to us, a Form class describes a form and determines how it works and appears.


In a similar way that a model class’s fields map to database fields, a form class’s fields map to
 HTML form <input> elements. (A ModelForm maps a model class’s fields to HTML form <input> elements 
 via a Form; this is what the Django admin is based upon.)

A form’s fields are themselves classes; they manage form data and perform validation when a form is
 submitted. A DateField and a FileField handle very different kinds of data and have to do 
  things with it.

A form field is represented to a user in the browser as an HTML “widget” - a piece of user inter
face machinery. Each field type has an appropriate default Widget class, but these can be overridden as required.

"""