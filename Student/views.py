from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,CreateView,UpdateView,ListView
from Student.forms import Stud_profileForm
from CarrierApp.models import Student,College,Course,Question,Answer,Mark
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from CarrierApp.models import *
# Create your views here.

class StudentHome(TemplateView):
    template_name='Stud_templates/indexs.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['project_count'] = Project.objects.filter(student=self.request.user).count()
    
        return context

class Stud_AddProfile(LoginRequiredMixin,CreateView):
    template_name='Stud_templates/Add_profile.html'
    form_class=Stud_profileForm
    model=Student
    success_url=reverse_lazy('Stud_home')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
        
class Stud_profileView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Student.objects.filter(user=id)
        return render(request,'Stud_templates/profileview.html',{"data": data})
    
class Stud_profileEdit(View):
    # template_name='Stud_templates/Add_profile.html'
    # form_class=Stud_profileForm
    # model=Student
    # success_url=reverse_lazy('Stud_home')
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Student.objects.get(user=id)
        form=Stud_profileForm(instance=data)  
        return render(request,'Stud_templates/Add_profile.html',{"form":form})  
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Student.objects.get(user=id)
        form=Stud_profileForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
        else:
            print("invalid")
        return redirect('Stud_home')     

class CollegeView(View):
    def get(self,request):
        data=College.objects.all()
        return render(request,'Stud_templates/CollegeView.html',{"data":data})
    
    
class CourseView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Course.objects.filter(College_name=id)
        return render(request,'Stud_templates/CourseView.html',{"data":data})
    
    

class AptitudeTestView(ListView):
    model = Question
    template_name = 'Stud_templates/aptitude_test.html'
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question__in=context['questions'])
        student_name = self.request.user.student_profile
        try:
            mark = Mark.objects.get(student_name=student_name)
        except Mark.DoesNotExist:
            mark = None
        context['mark'] = mark
        return context

    
    
    def post(self, request, *args, **kwargs):
        total_marks = self.calculate_total_marks(request.POST)
        student_name = request.user.student_profile  # Assuming user is authenticated and has student profile
        Mark.objects.create(student_name=student_name, Mark=total_marks)
        return redirect('Stud_home')  # Redirect to a page showing the result or any other desired page

    def calculate_total_marks(self, post_data):
        total_marks = 0
        for key, value in post_data.items():
            if key.startswith('answer_'):
                answer_id = int(value)
                answer = Answer.objects.get(id=answer_id)
                if answer.is_true:
                    total_marks += 5  # Assuming each correct answer contributes 1 mark
        return total_marks
    

class Collegelist_Mark(View):
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        student_data = Student.objects.filter(user=student_id)
        college_list = []

        for student in student_data:
            student_id = student.id
            marks = Mark.objects.filter(student_name=student_id)
            for mark in marks:
                aptitude_mark = mark.Mark
                colleges = College.objects.filter(cut_off_mark__lte=aptitude_mark)
                college_list.extend(colleges)



        return render(request, 'Stud_templates/filterd_college.html', {"data": college_list})       

from .models import *
from .forms import *
from django.http import JsonResponse
import os
import csv
import time

csv_file = "./Student/All_Streams_Ernakulam_Course_Colleges.csv"

class CourseRecommendationSystem:
    def __init__(self, csv_file):  # Fixed method name from _init_ to __init__
        self.courses = self.load_courses(csv_file)
        self.interest_map = {
            "Science": ["Engineering", "Medical", "Computer Science", "Basic Sciences"],
            "Commerce": ["Accounting", "Business Management", "Economics"],
            "Arts": ["Liberal Arts", "Design", "Law", "Media", "Social Work"],
            "Generic": ["Hospitality", "Event Management", "Digital Skills"]
        }

    def load_courses(self, csv_file):
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        courses = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    courses.append({
                        "stream": row["Stream"],
                        "course": row["Course"],
                        "college": row["College"]
                    })
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []
        
        return courses

    def print_bot_message(self, message):
        print("\nBot: ", end="")
        for char in message:
            print(char, end="", flush=True)
            time.sleep(0.01)  # Adds a typing effect
        print()

    def get_unique_streams(self):
        return sorted(list(set(course["stream"] for course in self.courses)))

    def get_recommendations(self, interest):
        filtered_courses = [course for course in self.courses if course["stream"].lower() == interest.lower()]
        
        if interest == "All Courses":
            return filtered_courses

        keywords = {
            "Engineering": ["B.Tech", "M.Tech", "B.Arch"],
            "Medical": ["MBBS", "BDS", "BAMS", "BHMS"],
            "Computer Science": ["Computer", "IT", "Data Science", "BCA"],
            "Basic Sciences": ["B.Sc."],
            "Accounting": ["B.Com", "CA"],
            "Business Management": ["BBA", "BMS", "Management"],
            "Economics": ["Economics", "Statistics"],
            "Liberal Arts": ["B.A."],
            "Design": ["Design", "Fine Arts"],
            "Law": ["Law", "LLB"],
            "Media": ["Media", "Journalism"],
            "Social Work": ["Social Work", "Education"],
            "Hospitality": ["Hotel"],
            "Event Management": ["Event"],
            "Digital Skills": ["Digital"]
        }

        if interest in keywords:
            return [
                course for course in filtered_courses 
                if any(keyword.lower() in course["course"].lower() for keyword in keywords[interest])
            ]
        return filtered_courses

import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class CareerGuidanceSystem:
    def __init__(self):
        # Initialize model and tokenizer
        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.df = pd.read_csv('./Student/truncated_career_recommender_dataset.csv')  # Use a relative path
        self.process_dataset()
        self.skill_vectorizer = TfidfVectorizer(stop_words='english')
        self.create_skill_vectors()

    def process_dataset(self):
        """Process the dataset to extract unique career paths and their requirements"""
        self.career_mapping = {}
        self.career_skills = {}

        for _, row in self.df.iterrows():
            spec = row['UG Specialization']
            career = row['Career Path']

            if pd.notna(spec) and pd.notna(career):
                self.career_mapping.setdefault(spec, set()).add(career)

            if pd.notna(career) and pd.notna(row['Skills']):
                skills = row['Skills'].split(';')
                self.career_skills.setdefault(career, set()).update(skills)

        # Convert sets to lists
        self.career_mapping = {k: list(v) for k, v in self.career_mapping.items()}
        self.career_skills = {k: list(v) for k, v in self.career_skills.items()}

    def create_skill_vectors(self):
        """Create TF-IDF vectors for skill matching"""
        career_skill_docs = {career: ' '.join(skills) for career, skills in self.career_skills.items()}
        self.skill_vectors = self.skill_vectorizer.fit_transform(career_skill_docs.values())
        self.career_list = list(career_skill_docs.keys())

    def get_career_recommendations(self, user_skills):
        """Get career recommendations based on skill similarity"""
        if not user_skills:
            return []

        user_skill_text = ' '.join(user_skills)
        user_vector = self.skill_vectorizer.transform([user_skill_text])

        # Calculate similarity with all careers
        similarities = cosine_similarity(user_vector, self.skill_vectors).flatten()

        # Get top matching careers
        career_scores = sorted(zip(self.career_list, similarities), key=lambda x: x[1], reverse=True)
        return career_scores

    def generate_recommendations(self, user_data):
        """Generate career recommendations based on user data"""
        recommendations = []
        specialization_careers = self.career_mapping.get(user_data['specialization'], [])
        skill_based_careers = self.get_career_recommendations(user_data['skills'])

        for career, score in skill_based_careers:
            if score > 0.1:  # Only include careers with significant match
                similar_profiles = self.df[self.df['Career Path'] == career]
                avg_score = similar_profiles['UG CGPA/Percentage'].mean()

                career_required_skills = self.career_skills.get(career, [])
                user_skill_set = set(skill.lower() for skill in user_data['skills'])
                missing_skills = [skill for skill in career_required_skills if skill.lower() not in user_skill_set]

                recommendations.append({
                    "career": career,
                    "match_score": score * 100,  # Convert to percentage
                    "avg_score_required": avg_score if not pd.isna(avg_score) else "N/A",
                    "missing_skills": missing_skills[:5],  # Top 5 missing skills
                    "similar_profiles_count": len(similar_profiles)
                })

        return recommendations

    def format_recommendations(self, name, recommendations):
        """Format recommendations for display"""
        if not recommendations:
            return f"Dear {name}, I couldn't find specific career matches. Consider improving your skills or exploring different fields."

        response = f"Dear {name}, here are your personalized career recommendations:\n\n"
        for i, rec in enumerate(recommendations[:5], 1):  # Top 5 recommendations
            response += f"{i}. {rec['career']}\n"
            response += f"   Match Score: {rec['match_score']:.1f}%\n"
            response += f"   Average Required Score: {rec['avg_score_required']}\n"
            if rec['missing_skills']:
                response += f"   Recommended skills to acquire: {', '.join(rec['missing_skills'])}\n"
            response += f"   Similar profiles in our database: {rec['similar_profiles_count']}\n\n"

        return response


def career_guidance(request):
    if request.method == 'POST':
        form = CareerPreferenceForm(request.POST)
        if form.is_valid():
            user_data = {
                'name': form.cleaned_data['name'],
                'education': form.cleaned_data['education'],
                'specialization': form.cleaned_data['specialization'],
                'skills': [skill.strip() for skill in form.cleaned_data['skills'].split(',') if skill.strip()],
                'score': float(form.cleaned_data['score']) if form.cleaned_data['score'] else None
            }

            career_system = CareerGuidanceSystem()
            recommendations = career_system.generate_recommendations(user_data)
            recommendations = career_system.generate_recommendations(user_data)
            print("Generated Recommendations:", recommendations)  # Check if the data is correct

            # career_names = [rec["career"] for rec in recommendations]
            # print("Recommended Careers:", career_names)
            return render(request, 'Stud_templates/career_results.html', {
                'recommendations': recommendations,
                'user_data': user_data
            })
    else:
        form = CareerPreferenceForm()

    return render(request, 'Stud_templates/career_guidance.html', {'form': form})
    # def __init__(self):
    #     pass
    
    # def get_career_recommendations(self, user_data):
    #     recommendations = []

    #     # Get career recommendations based on specialization
    #     spec_careers = self.career_mapping.get(user_data['specialization'], [])

    #     # Get career recommendations based on skills
    #     skill_based_careers = self.get_skill_recommendations(user_data['skills'])

    #     # Combine both types of recommendations
    #     for career, score in skill_based_careers:
    #         if score > 0.1:  # Only include careers with some skill match
    #             # Find similar profiles from the dataset
    #             similar_profiles = self.df[self.df['Career Path'] == career]
    #             avg_score = similar_profiles['UG CGPA/Percentage'].mean()

    #             # Get required and recommended skills
    #             career_required_skills = self.career_skills.get(career, [])
    #             user_skill_set = set(user_data['skills'])
    #             missing_skills = [skill for skill in career_required_skills
    #                             if skill.lower() not in [s.lower() for s in user_skill_set]]

    #             recommendations.append({
    #                 "career": career,
    #                 "match_score": score,
    #                 "avg_score_required": avg_score,
    #                 "missing_skills": missing_skills[:5],  # Top 5 missing skills
    #                 "similar_profiles_count": len(similar_profiles)
    #             })

    #     return self.format_recommendations(user_data['name'], recommendations)
    
    # def format_recommendations(self, name, recommendations):
    #     """Format recommendations for display"""
    #     if not recommendations:
    #         return f"Dear {name}, based on your profile, I couldn't find specific career matches. Consider exploring more skills or different specializations."

    #     response = f"Dear {name}, here are your personalized career recommendations:\n\n"
    #     for i, rec in enumerate(recommendations[:5], 1):  # Top 5 recommendations
    #         response += f"{i}. {rec['career']}\n"
    #         response += f"   Match Score: {rec['match_score']*100:.1f}%\n"
    #         response += f"   Average Required Score: {rec['avg_score_required']:.1f}%\n"
    #         if rec['missing_skills']:
    #             response += f"   Recommended skills to acquire: {', '.join(rec['missing_skills'])}\n"
    #         response += f"   Similar profiles in our database: {rec['similar_profiles_count']}\n\n"

    #     return response
    #     sample_recommendations = [
    #         {
    #             "career": "Software Developer",
    #             "match_score": 0.85,
    #             "avg_score_required": 75.5,
    #             "missing_skills": ["Docker", "GraphQL", "TypeScript"],
    #             "similar_profiles_count": 120
    #         },
    #         {
    #             "career": "Data Scientist",
    #             "match_score": 0.75,
    #             "avg_score_required": 80.2,
    #             "missing_skills": ["Spark", "Deep Learning", "NLP"],
    #             "similar_profiles_count": 85
    #         },
    #         {
    #             "career": "UI/UX Designer",
    #             "match_score": 0.68,
    #             "avg_score_required": 72.4,
    #             "missing_skills": ["Figma", "User Research", "Prototyping"],
    #             "similar_profiles_count": 65
    #         }
    #     ]
    #     return sample_recommendations



def course_guidance(request):
    course_system = CourseRecommendationSystem(csv_file)
    available_streams = course_system.get_unique_streams()
    
    if request.method == 'POST':
        stream = request.POST.get('stream')
        # interest = request.POST.get('interest')
        # print(f"Stream: {stream}, Interest: {interest}")
        if stream :
            recommendations = course_system.get_recommendations(stream)
            interests = course_system.interest_map.get(stream, []) + ["All Courses"]
            
            return render(request, 'Stud_templates/course_results.html', {
                'recommendations': recommendations,
                'stream': stream,
                # 'interest': interest,
                'available_streams': available_streams,
                'interests': interests
            })
            
    return render(request, 'Stud_templates/course_guidance.html', {
        'available_streams': available_streams
    })

def get_interests(request):
    if request.method == 'GET':
        stream = request.GET.get('stream')
        course_system = CourseRecommendationSystem(csv_file)
        interests = course_system.interest_map.get(stream, []) + ["All Courses"]
        return JsonResponse({'interests': interests})
    return JsonResponse({'error': 'Invalid request'}, status=400)
# def career_guidance(request):
#     if request.method == 'POST':
#         form = CareerPreferenceForm(request.POST)
#         if form.is_valid():
#             user_data = {
#                 'name': form.cleaned_data['name'],
#                 'education': form.cleaned_data['education'],
#                 'specialization': form.cleaned_data['specialization'],
#                 'skills': [skill.strip() for skill in form.cleaned_data['skills'].split(',')],
#                 'score': form.cleaned_data['score']
#             }
            
#             career_system = CareerGuidanceSystem()
#             raw_recommendations = career_system.get_career_recommendations(user_data)
            
#             # Convert list of tuples to structured dictionaries for the template
#             recommendations = [
#                 {
#                     "career": career[0],
#                     "match_score": career[1] * 100,  # Convert fraction to percentage
#                     "avg_score_required": 60,  # Placeholder for average score required
#                     "similar_profiles_count": 10,  # Placeholder for similar profiles count
#                     "missing_skills": []  # Placeholder for missing skills
#                 }
#                 for career in raw_recommendations
#             ]
            
#             return render(request, 'Stud_templates/career_results.html', {
#                 'recommendations': recommendations,
#                 'user_data': user_data
#             })
#     else:
#         form = CareerPreferenceForm()
        
#     return render(request, 'Stud_templates/career_guidance.html', {'form': form})
