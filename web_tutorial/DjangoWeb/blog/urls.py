from django.urls import path, re_path, register_converter
from . import views, converters

# register your custom converts
register_converter(converters.FourDigitYearConverter, "yyyy")
app_name = "blog"

# urlpatterns should be a Python list of path() and/or re_path() instances.

urlpatterns = [
    re_path(r'^$', views.blog_title, name="blog_title"),
    path('<int:article_id>', views.blog_article, name="blog_detail"),

    # adjust to use named regular expression instead of unnamed
    # re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
]