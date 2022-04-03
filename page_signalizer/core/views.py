from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Connection_Spec
from .forms import Connection_Spec_CreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home_page(request):
    templates = Connection_Spec.objects.filter(owner=request.user)
    context = {'templates': templates}
    
    return render(request, 'core/home.html', context)


# login require in urls.py
class Render_add(CreateView):
    model = Connection_Spec
    fields = ['name', 'url', 'seq', 'interval_seconds', 'max_cycles', 'rand', 'eta' , 'title','msg']
    template_name = 'core/add.html'


    def form_valid(self, form):
        # posted_by is a name in the model
        # self.request_user - obligatory form to automate user association
        form.instance.owner = self.request.user
        return super().form_valid(form)



@login_required
def render_scrape(request, id):
    template = Connection_Spec.objects.get(id=id)
    is_request_by_owner = request.user == template.owner
    context = {'template': template}

    if is_request_by_owner:
        return render(request, 'core/scrape.html', context)
    else:
        return render(request, 'core/permissions_denied.html', context)

@login_required
def update_template(request, id):
    template = Connection_Spec.objects.get(id=id)
    form = Connection_Spec_CreationForm(request.POST or None, instance=template)
    is_request_by_owner = request.user == template.owner

    if form.is_valid():
        form.save()
        return redirect('/')
    
    context = {'form': form, 
                'template':template,
                'is_permitted': is_request_by_owner}

    return render(request, 'core/update.html', context)


@login_required
def delete_template(request, id):
    template = Connection_Spec.objects.get(id=id)
    is_request_by_owner = request.user == template.owner

    context = {'template':template,
                'is_permitted': is_request_by_owner}

    if request.method == "POST":
        template.delete()
        return redirect('core:home')
    
    
    return render(request, 'core/delete_form.html', context)


