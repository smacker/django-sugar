# -*- mode: python; coding: utf-8; -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader

from sugar.views.json import JsonResponse

from django.utils.translation import ugettext_lazy as _

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps


def render_to(template_path):
    """
    Decorator for Django views that sends returned dict to render_to_response
    function with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use

    Examples::
      from sugar.views.decorators import render_to, ajax_request
      
      @render_to('some/tmpl.html')
      def view(request):
          if smth:
              return {'context': 'dict'}
          else:
              return {'context': 'dict'}, 'other/tmpl.html'

    (c) 2006-2009 Alexander Solovyov, new BSD License
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                template = output[1]
                output_dict = output[0]
            elif isinstance(output, dict):
                output_dict = output
                if 'TEMPLATE' in output:
                    template = output.pop('TEMPLATE')
                else:
                    template = template_path
            else:
                return output
            if request.GET.has_key('inline'):
                template_parts = template.rsplit('/', 1)
                template = template_parts[0] + '/inline/' + template_parts[1]
            return render_to_response(template, output_dict,
                                          RequestContext(request))
        wrapper.__name__ = func.__name__
        wrapper.__module__ = func.__module__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return renderer
    
def ajax_request(func):
    """
    Checks request.method is POST. Return error in JSON in other case.

    If view returned dict, returns JsonResponse with this dict as content.
    Examples::
    
    from sugar.views.decorators import render_to, ajax_request
    from sugar.views.helpers import get_object_or_404_ajax
    
    @ajax_request
    def comment_edit(request, object_id):
        comment = get_object_or_404_ajax(CommentNode, pk=object_id)
        if request.user != comment.user:
            return {'error': {'type': 403, 'message': 'Access denied'}}
        if 'get_body' in request.POST:
            return {'body': comment.body}
        elif 'body' in request.POST:
            comment.body = request.POST['body']
            comment.save()
            return {'body_html': comment.body_html}
        else:
            return {'error': {'type': 400, 'message': 'Bad request'}}
    
    
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            response = func(request, *args, **kwargs)
        else:
            response = {'error': {'type': 405,
                                  'message': 'Accepts only POST request'}}
        if isinstance(response, dict):
            resp = JsonResponse(response)
            if 'error' in response:
                resp.status_code = response['error'].get('type', 500)
            return resp
        return response
    wrapper.__name__ = func.__name__
    wrapper.__module__ = func.__module__
    wrapper.__doc__ = func.__doc__
    return wrapper


def render_from(template_path):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            else:
                template = template_path
            kwargs = {'context_instance': RequestContext(request)}
            return loader.render_to_string(template, output, **kwargs)
        return wrapper
    return decorator


def default_context(request, title=_('Are you sure?'), text='',\
                        submit=_('Confirm'), back=None, extra=dict()):
    context = {
           'title': title,
           'text': text,
           'submit': submit,
           'back': back,
           }

    context.update(extra)

    return RequestContext(request, context)

def confirm_required(template_name='confirm.html', context_creator=default_context, key='__confirm__'):
    """
    http://djangosnippets.org/snippets/1922/

    Decorator for views that need confirmation page. For example, delete
    object view. Decorated view renders confirmation page defined by template
    'template_name'. If request.POST contains confirmation key, defined
    by 'key' parameter, then original view is executed.

    Context for confirmation page is created by function 'context_creator',
    which accepts same arguments as decorated view.

    Example
    -------

        def remove_file_context(request, id):
            file = get_object_or_404(Attachment, id=id)
            return RequestContext(request, {'file': file})

        @confirm_required('remove_file_confirm.html', remove_file_context)
        def remove_file_view(request, id):
            file = get_object_or_404(Attachment, id=id)
            file.delete()
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)



    Example of HTML template
    ------------------------

        <h1>Remove file {{ file }}?</h1>

        <form method="POST" action="">
            <input type="hidden" name="__confirm__" value="1" />
            <input type="submit" value="delete"/> <a href="{{ file.get_absolute_url }}">cancel</a>
        </form>

    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.POST.has_key(key):
                return func(request, *args, **kwargs)
            else:
                context = context_creator and context_creator(request, *args, **kwargs) \
                    or RequestContext(request)
                return render_to_response(template_name, context)
        return wraps(func)(inner)
    return decorator
