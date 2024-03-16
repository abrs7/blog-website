from django import forms
from .models import Post, Comment, Profile
from django.core.validators import MaxValueValidator


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'profile_pic',  'occupation', 'phone', 'github', 'website_url', 'twitter_url',  'facebook_url', 'instagram_url', 'bio', 'linkedin_url', 'location', 'birth_date', 'programming_proficiency','problem_solving','critical_thinking','communication_skills','adaptability','attention_to_detail')

        programming_proficiency = forms.IntegerField(validators=[MaxValueValidator(100)], label='Programming Proficiency', widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
        problem_solving = forms.IntegerField(validators=[MaxValueValidator(100)], label='Problem Solving', widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
        critical_thinking = forms.IntegerField(validators=[MaxValueValidator(100)], label='Critical Thinking', widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
        communication_skills = forms.IntegerField(validators=[MaxValueValidator(100)], label='Communication Skills', widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
        adaptability = forms.IntegerField(validators=[MaxValueValidator(100)], label='Adaptability', widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
        attention_to_detail = forms.IntegerField(validators=[MaxValueValidator(100)], label='Attention to Detail', widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
    
  
class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Exclude 'slug' field

    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.slug = self.generate_unique_slug()
        instance.status = 1
        if commit:
            instance.save()
        return instance

    def generate_unique_slug(self):
        base_slug = 'blog'
        counter = 1
        slug = base_slug
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}_{counter}"
            counter += 1
        return slug


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body' : forms.Textarea()
        }        