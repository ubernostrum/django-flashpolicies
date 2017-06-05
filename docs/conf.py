import os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'django-flashpolicies'
copyright = u'2009-2017, James Bennett'
version = '1.9'
release = '1.9'
exclude_trees = ['_build']
pygments_style = 'sphinx'
html_static_path = ['_static']
htmlhelp_basename = 'django-flashpoliciesdoc'
latex_documents = [
  ('index', 'django-flashpolicies.tex', u'django-flashpolicies Documentation',
   u'James Bennett', 'manual'),
]
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

