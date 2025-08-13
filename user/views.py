from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse, reverse_lazy

from user.forms import ProfileForm, UserLoginForm, UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin



class UserLoginView(LoginView):
  template_name = 'user/login.html'
  form_class = UserLoginForm

  def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
  def form_valid(self, form):
      user = form.get_user()

      if user:
        auth.login(self.request, user)

        messages.success(self.request, f'{user.username} Вы вошли в аккаунт')
        
        return HttpResponseRedirect(self.get_success_url())
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Gladius - Авторизация'
      return context


class UserRegisterView(CreateView):
   template_name = 'user/registration.html'
   form_class = UserRegisterForm
   success_url = reverse_lazy('user:profile')

   def form_valid(self, form):
       
       user = form.instance

       if user:
          form.save()
          auth.login(self.request, user)
        
       messages.success(self.request, f'{user.username} Вы успешно зарегистрировались')

       return HttpResponseRedirect(self.success_url)
   
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["title"] = 'Gladius - Регистрация'
       return context


class UserProfileView(LoginRequiredMixin,UpdateView):
   template_name = 'user/profile.html'
   form_class = ProfileForm
   success_url = reverse_lazy("user:profile")

   def get_object(self, queryset = None):
      return self.request.user
   
   def form_valid(self, form):
       messages.success(self.request, 'Профиль успешно обновлён')
       return super().form_valid(form)
   
   def form_invalid(self, form):
       messages.error(self.request, 'Произошла ошибка')
       return super().form_invalid(form)
   
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["title"] = 'Gladius - Кабинет'
       return context


@login_required
def logout(request):
   auth.logout(request)
   messages.success(request, 'Вы успешно вышли с аккаунта')
   return redirect(reverse('main:index'))