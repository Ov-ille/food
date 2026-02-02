import json
from dal import autocomplete
from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.options import csrf_protect_m
from django.forms import BaseModelFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path, resolve, reverse
from django.utils.decorators import classonlymethod
from django.utils.functional import classproperty
from django.views import View
from django.views.generic import TemplateView

from food.forms import FoodForm, IngredientForm, RecipeForm, UnitForm
from food.models import Food, Ingredient, Recipe, Unit


class StandardModelView(View):

    model = None 
    form_class = None
    inlines = []
    url_roles = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opts = self.model._meta

    @classonlymethod
    def as_view(cls):
        return super().as_view()
    
    @classproperty
    def base_url(cls):
        # todo
        return cls.model._meta.model_name
    
    @classmethod
    def build_url_name(self, role):
        return f"{self.base_url}_{role}"
    
    @classmethod
    def url_pattern(cls, role):
        if role == "add":
            return f"{cls.base_url}/add/"
        elif role == "change":
            return f"{cls.base_url}/<path:object_id>/change/"
        elif role == "list":
            return f"{cls.base_url}/"
        elif role == "delete":
            return f"{cls.base_url}/<path:object_id>/delete/"
        # todo: other
    
    @classonlymethod
    def get_urls(cls):
        return [path(
                cls.url_pattern(role),
                cls.as_view(),
                name=cls.build_url_name(role)
            ) for role in cls.url_roles]
    
    def get(self, request, object_id=None):
        role = resolve(request.path).url_name.split("_", maxsplit=1)[-1]
        if role in ["add", "change"]:
            return self.add_change_view(request, object_id)
        elif role == "list":
            return self.list_view(request)
        elif role == "delete":
            return self.delete_view(request, object_id)

    
    def post(self, request, object_id=None):
        role = resolve(request.path).url_name.split("_", maxsplit=1)[-1]
        if role in ["add", "change"]:
            return self.add_change_view(request, object_id)
        elif role == "delete":
            return self.delete_view(request, object_id)

    def get_object(self, object_id):
        try:
            object_id = int(object_id)
            return self.model.objects.get(pk=object_id)
        except (ValueError, self.model.DoesNotExist):
            # todo
            raise Exception("Cant parse ID or Object does not exist!")
        
    @property
    def media(self):
        js = [
            "vendor/jquery/jquery.js",
        ]
        return forms.Media(js=["admin/js/%s" % url for url in js])
    
    @csrf_protect_m
    def list_view(self, request):
        return HttpResponse(
            render(
                request,
                "food/list.html",
                context={
                    "title": f"All {self.model._meta.verbose_name_plural}",
                    "objects": self.model.objects.all(),
                    "add_url": f"food:{self.build_url_name("add")}",
                    "change_url": f"food:{self.build_url_name("change")}",
                    }
        ))

    def get_form(self, object, editable, data=None):
        return self.form_class(
            prefix=self.model._meta.model_name, 
            instance=object,
            data=data,
            editable=editable
        )
    
    def get_inline_formsets(self, object, editable, has_delete_permission, data=None):
        inline_formsets = []
        for inline in self.inlines:
            InlineFormset = inlineformset_factory(
                self.model, 
                inline.model, 
                inline.form_class, 
                extra=0,    
                can_delete=editable and has_delete_permission, 
                validate_max=True
                )
            inline_formset = InlineFormset(
                prefix=inline.model._meta.model_name, 
                instance=object, 
                data=data,
                queryset=inline.model.objects.none() if not object and not data else None,
                form_kwargs={"editable": editable}
                )
            inline_formset.opts = inline.model._meta
            inline_formsets.append(inline_formset)
        return inline_formsets

    @csrf_protect_m
    def delete_view(self, request, object_id):
        object = self.get_object(object_id)
        object.opts = object._meta

        # todo: permission!
        has_delete_permission = True

        if not has_delete_permission:
            messages.warning(request, f"You don't have permission to delete this!")
            return HttpResponseRedirect(reverse(f"food:{self.build_url_name("change")}", kwargs={"object_id": object.pk} ))

        if request.method == "GET":
            return HttpResponse(
                render(
                    request,
                    "food/delete.html",
                    context={
                        "object": object,
                        "delete_url": f"food:{self.build_url_name("delete")}",
                        "change_url": f"food:{self.build_url_name("change")}",
                        }
            ))
        elif request.method == "POST":
            object.delete()
            messages.info(request, f"{object._meta.verbose_name} {str(object)} sucessfully deleted!")
            return HttpResponseRedirect(reverse(f"food:{self.build_url_name("list")}"))
 
    @csrf_protect_m
    def add_change_view(self, request, object_id=None):
        add = object_id is None

        # edit: currently in edit mode
        # editable: can edit
        # has_change_permission: can edit
        edit_mode = False
        if request.GET.get("e", 0) == "1" or add:
            edit_mode = True

        # popup
        popup = False
        if request.GET.get("p", 0) == "1":
            popup = True

        # todo: permissions
        has_change_permission = True
        has_delete_permission = True
        has_add_permission = True
        has_view_permission = True

        if not has_view_permission:
            ...

        if not has_change_permission:
            edit_mode = False

        if add:
            object = None
        else:
            object = self.get_object(object_id)

        if request.method == "GET":
            if popup:
                edit_mode = True
            form = self.get_form(object, edit_mode)
            inline_formsets = self.get_inline_formsets(object, edit_mode, has_delete_permission)

        elif request.method == "POST":
            form = self.get_form(object, edit_mode, data=request.POST)
            form_validated = form.is_valid()

            if form_validated:
                new_object = form.save(commit=False)
            else:
                new_object = form.instance

            inline_formsets = self.get_inline_formsets(object, edit_mode, has_delete_permission, request.POST)
            inline_formsets_validated = all([x.is_valid() for x in inline_formsets])

            if inline_formsets_validated and form_validated:
                obj = form.save()
                for inline_formset in inline_formsets:
                    inline_formset.instance = new_object
                    inline_formset.save()
                if popup and add:
                    popup_response_data = json.dumps({"add_change": "add" if add else "change", "id": obj.pk, "text": str(obj)})
                    return TemplateResponse(
                        request,
                        "food/popup_response.html",
                        {"popup_response_data": popup_response_data}
                    )
                return HttpResponseRedirect(reverse(f"food:{self.build_url_name("change")}", kwargs={"object_id": new_object.id}))

        media = self.media + form.media
        for inline_formset in inline_formsets:
            media += inline_formset.media

        context = {
            "form": form, 
            "inline_formsets": inline_formsets, 
            "add": add, 
            "edit_mode": edit_mode,
            "has_change_permission": has_change_permission,
            "has_delete_permission": has_delete_permission,
            "title_list": f"Show all {self.model._meta.verbose_name_plural}",
            "title": f"{'Add' if add else 'Change'} {self.model._meta.verbose_name}",
            "list_url": f"food:{self.build_url_name("list")}",
            "change_url": f"food:{self.build_url_name("change")}",
            "delete_url": f"food:{self.build_url_name("delete")}",
            "model_opts": self.opts,
            "media": media,
            "popup": popup
        }

        return HttpResponse(render(request,
                                "food/add_change.html",
                                context=context))


class IngredientView(StandardModelView):
    model = Ingredient
    form_class = IngredientForm
    url_roles = ["add"]

class FoodView(StandardModelView):
    model = Food
    form_class = FoodForm
    url_roles = ["add"]

class UnitView(StandardModelView):
    model = Unit
    form_class = UnitForm
    url_roles = ["add"]

class RecipeView(StandardModelView):
    model = Recipe
    form_class = RecipeForm
    inlines = [IngredientView]
    url_roles = ["add", "change", "list", "delete"]



class FoodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # todo: permissions
        qs = Food.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs