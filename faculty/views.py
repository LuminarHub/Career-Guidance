from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CarrierApp.models import *
from django.views.generic import TemplateView
from .utils import *
# Create your views here.

class Fac_HomeView(TemplateView):
    template_name = 'fac_home.html'


def videos_view(request):
    videos = Videos.objects.filter(user=request.user)
    for video in videos:
        video.embed_url = get_youtube_embed_url(video.video_url)
    return render(request, 'videos.html', {'videos': videos})

def all_videos_view(request):
    videos = Videos.objects.all()
    for video in videos:
        video.embed_url = get_youtube_embed_url(video.video_url)
    return render(request, 'all_videos.html', {'videos': videos})

def all_videos_admin_view(request):
    videos = Videos.objects.all()
    for video in videos:
        video.embed_url = get_youtube_embed_url(video.video_url)
    return render(request, 'admin_videos.html', {'videos': videos})


def video_detail_view(request, video_id):
    video = get_object_or_404(Videos, id=video_id)
    video.embed_url = get_youtube_embed_url(video.video_url)
    return render(request, 'video_detail.html', {'video': video})

@login_required
def add_video_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        text = request.POST.get('text')
        if not video_url:
            messages.error(request, 'Video URL is required')
            return render(request, 'add_video.html')
        if not is_youtube_url(video_url):
            messages.error(request, 'Please provide a valid YouTube URL')
            return render(request, 'add_video.html', {'video_url': video_url, 'text': text})
        Videos.objects.create(
            video_url=video_url,
            text=text,
            user=request.user  
        )
        
        messages.success(request, 'Video has been added successfully')
        return redirect('videos')
    
    return render(request, 'add_video.html')

@login_required
def update_video_view(request, video_id):
    video = get_object_or_404(Videos, id=video_id)
    if video.user != request.user:
        messages.error(request, 'You do not have permission to edit this video')
        return redirect('videos')
    
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        text = request.POST.get('text')
        
        # Validation
        if not video_url:
            messages.error(request, 'Video URL is required')
            return render(request, 'update_video.html', {'video': video})
        
        if not is_youtube_url(video_url):
            messages.error(request, 'Please provide a valid YouTube URL')
            video.video_url = video_url  
            video.text = text
            return render(request, 'videos/update_video.html', {'video': video})
        
        # Update video
        video.video_url = video_url
        video.text = text
        video.save()
        
        messages.success(request, 'Video has been updated successfully')
        return redirect('video_detail', video_id=video.id)
    
    return render(request, 'update_video.html', {'video': video})

# Delete a video
@login_required
def delete_video_view(request, video_id):
    video = get_object_or_404(Videos, id=video_id)
    if video.user != request.user:
        messages.error(request, 'You do not have permission to delete this video')
        return redirect('videos')
    
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video has been deleted successfully')
        return redirect('videos')
    video.embed_url = get_youtube_embed_url(video.video_url)
    return render(request, 'delete_video.html', {'video': video})

from .forms import *
# Student Views
@login_required
def student_projects(request):
    projects = Project.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'list.html', {'projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = request.user
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('student_projects')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, student=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('student_projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, student=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('student_projects')
    return render(request, 'delete_project.html', {'project': project})


@login_required
def faculty_view_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'project_view.html', {'projects': projects})

@login_required
def admin_view_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'admin_list_projects.html', {'projects': projects})

@login_required
def faculty_view_student_projects(request, student_id):
    projects = Project.objects.filter(student_id=student_id).order_by('-created_at')
    return render(request, 'student_projects.html', {'projects': projects})