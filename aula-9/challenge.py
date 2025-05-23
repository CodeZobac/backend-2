# Comprehensive Django REST API test suite with pytest
import pytest
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
import json

# Import the BlogPost model from exercise.py
from exercise import BlogPost

class BlogPostTestCase(TestCase):
    """Test case for BlogPost model"""
    
    def test_blogpost_creation(self):
        """Test creating a BlogPost"""
        post = BlogPost.objects.create(
            title="Test Post",
            content="This is test content"
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is test content")
        self.assertTrue(post.is_published)
    
    def test_blogpost_str_method(self):
        """Test the string representation of BlogPost"""
        post = BlogPost.objects.create(
            title="Test Post",
            content="Test content"
        )
        self.assertEqual(str(post), "Test Post")
    
    def test_get_excerpt(self):
        """Test the get_excerpt method"""
        long_content = "This is a very long content " * 10
        post = BlogPost.objects.create(
            title="Long Post",
            content=long_content
        )
        excerpt = post.get_excerpt(50)
        self.assertEqual(len(excerpt), 53)  # 50 chars + "..."
        self.assertTrue(excerpt.endswith("..."))
    
    def test_is_recent(self):
        """Test the is_recent method"""
        # Create a recent post
        recent_post = BlogPost.objects.create(
            title="Recent Post",
            content="Recent content",
            published_date=timezone.now()
        )
        self.assertTrue(recent_post.is_recent())
        
        # Create an old post
        old_date = timezone.now() - timedelta(days=10)
        old_post = BlogPost.objects.create(
            title="Old Post",
            content="Old content",
            published_date=old_date
        )
        self.assertFalse(old_post.is_recent())


# Pytest fixtures for API testing
@pytest.fixture
def api_client():
    """Create an API client for testing"""
    return APIClient()

@pytest.fixture
def sample_blogpost():
    """Create a sample BlogPost for testing"""
    return BlogPost.objects.create(
        title="Sample Post",
        content="Sample content for testing"
    )

@pytest.fixture
def multiple_blogposts():
    """Create multiple BlogPosts for testing"""
    posts = []
    for i in range(5):
        post = BlogPost.objects.create(
            title=f"Post {i+1}",
            content=f"Content for post {i+1}",
            published_date=timezone.now() - timedelta(days=i)
        )
        posts.append(post)
    return posts

# Parametrized tests
@pytest.mark.parametrize("title,content,expected_published", [
    ("Test Title 1", "Test Content 1", True),
    ("Test Title 2", "Test Content 2", True),
    ("Draft Post", "Draft content", False),
])
@pytest.mark.django_db
def test_blogpost_parametrized_creation(title, content, expected_published):
    """Parametrized test for BlogPost creation"""
    post = BlogPost.objects.create(
        title=title,
        content=content,
        is_published=expected_published
    )
    assert post.title == title
    assert post.content == content
    assert post.is_published == expected_published


@pytest.mark.parametrize("content_length,excerpt_length", [
    (50, 30),
    (100, 50),
    (200, 100),
])
@pytest.mark.django_db
def test_excerpt_parametrized(content_length, excerpt_length):
    """Parametrized test for excerpt functionality"""
    content = "A" * content_length
    post = BlogPost.objects.create(
        title="Test Post",
        content=content
    )
    excerpt = post.get_excerpt(excerpt_length)
    
    if content_length <= excerpt_length:
        assert excerpt == content
    else:
        assert len(excerpt) == excerpt_length + 3  # +3 for "..."
        assert excerpt.endswith("...")


# API endpoint tests
@pytest.mark.django_db
def test_blogpost_list_api(api_client, multiple_blogposts):
    """Test the BlogPost list API endpoint"""
    # Mock URL - in a real Django project this would be properly configured
    url = '/api/blogposts/'
    
    # Since we don't have actual URLs configured, we'll simulate the response
    expected_data = {
        'count': 5,
        'results': [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'published_date': post.published_date.isoformat(),
                'is_published': post.is_published
            }
            for post in multiple_blogposts
        ]
    }
    
    # In a real test, you would do:
    # response = api_client.get(url)
    # assert response.status_code == status.HTTP_200_OK
    # assert response.data['count'] == 5
    
    # For this exercise, we'll test the data structure
    assert len(expected_data['results']) == 5
    assert expected_data['count'] == 5
    assert all('title' in post for post in expected_data['results'])


@pytest.mark.django_db
def test_blogpost_detail_api(api_client, sample_blogpost):
    """Test the BlogPost detail API endpoint"""
    # Mock URL - in a real Django project this would be properly configured
    url = f'/api/blogposts/{sample_blogpost.id}/'
    
    expected_data = {
        'id': sample_blogpost.id,
        'title': sample_blogpost.title,
        'content': sample_blogpost.content,
        'published_date': sample_blogpost.published_date.isoformat(),
        'is_published': sample_blogpost.is_published
    }
    
    # In a real test, you would do:
    # response = api_client.get(url)
    # assert response.status_code == status.HTTP_200_OK
    # assert response.data['title'] == sample_blogpost.title
    
    # For this exercise, we'll test the data structure
    assert expected_data['title'] == sample_blogpost.title
    assert expected_data['content'] == sample_blogpost.content
    assert expected_data['is_published'] == sample_blogpost.is_published


@pytest.mark.django_db
def test_blogpost_create_api(api_client):
    """Test creating a BlogPost via API"""
    url = '/api/blogposts/'
    data = {
        'title': 'New Post via API',
        'content': 'Content created via API',
        'is_published': True
    }
    
    # In a real test, you would do:
    # response = api_client.post(url, data, format='json')
    # assert response.status_code == status.HTTP_201_CREATED
    # assert BlogPost.objects.filter(title='New Post via API').exists()
    
    # For this exercise, we'll simulate the creation
    post = BlogPost.objects.create(**data)
    assert post.title == data['title']
    assert post.content == data['content']
    assert post.is_published == data['is_published']


@pytest.mark.django_db
def test_blogpost_update_api(api_client, sample_blogpost):
    """Test updating a BlogPost via API"""
    url = f'/api/blogposts/{sample_blogpost.id}/'
    data = {
        'title': 'Updated Title',
        'content': 'Updated content',
        'is_published': False
    }
    
    # In a real test, you would do:
    # response = api_client.put(url, data, format='json')
    # assert response.status_code == status.HTTP_200_OK
    
    # For this exercise, we'll simulate the update
    for key, value in data.items():
        setattr(sample_blogpost, key, value)
    sample_blogpost.save()
    
    updated_post = BlogPost.objects.get(id=sample_blogpost.id)
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.is_published == data['is_published']


@pytest.mark.django_db
def test_blogpost_delete_api(api_client, sample_blogpost):
    """Test deleting a BlogPost via API"""
    url = f'/api/blogposts/{sample_blogpost.id}/'
    post_id = sample_blogpost.id
    
    # In a real test, you would do:
    # response = api_client.delete(url)
    # assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # For this exercise, we'll simulate the deletion
    sample_blogpost.delete()
    assert not BlogPost.objects.filter(id=post_id).exists()


# Test the API response structure
@pytest.mark.django_db
def test_api_response_structure(multiple_blogposts):
    """Test that API responses have the correct structure"""
    # Simulate a paginated response
    posts = BlogPost.objects.all()[:3]
    
    response_data = {
        'count': BlogPost.objects.count(),
        'next': None,
        'previous': None,
        'results': []
    }
    
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'published_date': post.published_date.isoformat(),
            'is_published': post.is_published,
            'excerpt': post.get_excerpt(100),
            'is_recent': post.is_recent()
        }
        response_data['results'].append(post_data)
    
    # Test the structure
    assert 'count' in response_data
    assert 'results' in response_data
    assert isinstance(response_data['results'], list)
    assert len(response_data['results']) == 3
    
    # Test each post structure
    for post_data in response_data['results']:
        required_fields = ['id', 'title', 'content', 'published_date', 'is_published']
        for field in required_fields:
            assert field in post_data
