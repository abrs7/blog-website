from django import forms
from .models import Post

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
