from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,CreateView,FormView
from CarrierApp.models import *
from Admin.forms import AnswerForm,QuestionForm
from django.urls import reverse_lazy



from django.views.generic import TemplateView
from django.db.models import Count
import json
from .models import *

class AdminHome(TemplateView):
    template_name = 'Admin_temp/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Count statistics
        context['colleges_count'] = College.objects.count()
        context['students_count'] = Student.objects.count()
        context['questions_count'] = Question.objects.count()
        context['projects_count'] = Project.objects.count()
        
        # Recent data
        context['recent_students'] = Student.objects.all().order_by('-id')[:5]
        context['recent_projects'] = Project.objects.all().order_by('-created_at')[:4]
        context['recent_videos'] = Videos.objects.all().order_by('-id')[:3]
        
        # Data for college type chart
        college_types = College.objects.values('Type').annotate(count=Count('id'))
        labels = [college['Type'] for college in college_types]
        series = [college['count'] for college in college_types]
        
        context['college_types_data'] = json.dumps({
            'labels': labels,
            'series': series
        })
        
        return context
class StudentList(View):
    def get(self,request):
        data=Student.objects.all()
        return render(request,'Admin_temp/studentlist.html',{"data":data})
class StudentDelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')   
        student_instance = Student.objects.get(id=id)
        user_instance = student_instance.user
        student_instance.delete()
        user_instance.delete()
        return redirect('student_list') 
    
class CollegeList(View):
    def get(self,request):
        data=College.objects.all()
        return render(request,'Admin_temp/collegelist.html',{"data":data})
class CollegeDelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')   
        college_instance = College.objects.get(id=id)
        user_instance = college_instance.user

        # Delete the College instance and its associated Login instance
        college_instance.delete()
        user_instance.delete()
        return redirect('college_list')
    
class AddQuestion(CreateView):
    template_name='Admin_temp/Add_questions.html'  
    form_class=QuestionForm
    model=Question
    success_url=reverse_lazy('Add_question') 

class AddAnswer(FormView):
    template_name='Admin_temp/Add_answer.html'  
    form_class=AnswerForm
    # model=Answer
    # success_url=reverse_lazy('Add_answer')  
    def post(self,request):
        form=AnswerForm(request.POST)
        if form.is_valid():
            Answer.objects.create(**form.cleaned_data) 
        else:
            print("invalid")
        return redirect('Add_answer')        
      
class Questionlist(View):
    def get(self,request):
        data=Question.objects.all()
        return render(request,'Admin_temp/Questionlist.html',{"data":data})
    
class QuestionDelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')    
        Question.objects.get(id=id).delete()
        return redirect('Q_view')
    
class ACourseView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Course.objects.filter(College_name=id)
        return render(request,'Admin_temp/course.html',{"data":data})    

          

             




