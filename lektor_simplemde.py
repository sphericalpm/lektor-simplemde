import email

import pkg_resources
from flask import Blueprint, render_template_string
from lektor.admin.modules import dash
from lektor.pluginsystem import Plugin


TEMPLATE = '''
{% extends "dash.html" %}
{% block scripts %}
  {{ super() }}
  <link rel="stylesheet" href="//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
  <script src="//cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>
  <script>
    (new MutationObserver(function() {
        [...document.getElementsByTagName('textarea')].forEach(e => {
            if (e.className === 'form-control') {
                e.classList.add('simplemde-attached');
                let editor = new SimpleMDE({ element: e });
                editor.codemirror.on('change', () => {
                    // update textarea value
                    e.value = editor.value();

                    // dispatch syntetic event for react to update its state
                    let ev = new Event('input', { bubbles: true });
                    ev.simulated = true;
                    e.dispatchEvent(ev);
                });
            };
        });
    })).observe(
        document.getElementsByTagName('body')[0],
        {
            subtree: true,
            childList: true
        },
    );
  </script>
{% endblock %}
'''


def get_description(mod):
    distribution = pkg_resources.get_distribution(mod)
    if distribution.has_metadata('PKG-INFO'):
        meta = distribution.get_metadata('PKG-INFO')
    elif distribution.has_metadata('METADATA'):
        meta = distribution.get_metadata('METADATA')
    else:
        return None
    return email.message_from_string(meta).get('Summary', None)


def patched_endpoint(*args, **kwargs):
    return render_template_string(TEMPLATE)


class SimpleMdePlugin(Plugin):
    name = 'SimpleMDE'
    description = get_description(__module__)

    def on_server_spawn(self, *args, **kwargs):
        # remove all rule besides first one which is edit redirect
        while len(dash.bp.deferred_functions) > 1:
            dash.bp.deferred_functions.pop()
        # ... and fill all the rules back with our wrapper template
        for path, endpoint in dash.endpoints:
            dash.bp.add_url_rule(path, endpoint, patched_endpoint)
