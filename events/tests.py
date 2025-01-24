
from django.test import TestCase
from events.models import Event
from users.models import User
from rest_framework import status
from rest_framework.test import APIClient

# # Create your tests here.
class EventTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='super', password='super')
        User.objects.create_user(username='user1', password='user1')
        Event.objects.create(name='Korea series final', description='Who\'s gonna winner', category='sports', open=True, start_at='2025-01-26', end_at='2025-01-31')
        Event.objects.create(name='Ariana Grande Concert', description='The queen is coming', category='concert', open=True, start_at='2025-01-22', end_at='2025-01-31')
        Event.objects.create(name='Champions league final', description='Let\'s go Sonny', category='sports', open=True, start_at='2025-01-23', end_at='2025-01-23')
        Event.objects.create(name='Awesome play', description='Awesome', category='play', open=False, start_at='2024-01-23', end_at='2024-01-23')

    # create
    def test_create_event_success(self):
        user = User.objects.get(username='super')
        client = APIClient()
        client.force_authenticate(user=user) # Force user authenticated
        response = client.post('/api/v1/events/', {
          "name": "Hisaishi Joe ghibli concert",
          "description": "Ghibli studio music",
          "category": "orchestra",
          "open": "true",
          "start_at": "2025-02-02",
          "end_at": "2025-02-04"
        })

        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        saved_event = response.json()
        self.assertIsNotNone(saved_event)
        self.assertEqual(saved_event['name'], 'Hisaishi Joe ghibli concert')

    def test_category_not_in_choices_fails_to_create_event(self):
        user = User.objects.get(username='super')
        client = APIClient()
        client.force_authenticate(user=user)  # Force user authenticated
        response = client.post('/api/v1/events/', {
            "name": "Hisaishi Joe ghibli concert",
            "description": "Ghibli studio music",
            "category": "random",
            "open": "true",
            "start_at": "2025-02-02",
            "end_at": "2025-02-04"
        })

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)

    def test_admin_user_can_only_create_event(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user=user)
        response = self.client.post('/api/v1/events/', {
            "name": "Hisaishi Joe ghibli concert",
            "description": "Ghibli studio music",
            "category": "random",
            "open": "true",
            "start_at": "2025-02-02",
            "end_at": "2025-02-04"
        })

        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)

    # list
    def test_get_events_list_success(self):
        response = self.client.get('/api/v1/events/') # 가장 최근 거를 기본적으로 먼저 가져옴
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        event = response.json()
        self.assertTrue(event['count'] == 3)
        self.assertEqual(event['results'][2]['description'], 'Who\'s gonna winner')

    # retrieve
    def test_get_single_event_success(self):
        event = Event.objects.get(name='Ariana Grande Concert')
        response = self.client.get(f'/api/v1/events/{event.id}/')
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        event = response.json()
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'Ariana Grande Concert')


    def test_single_event_not_found_with_wrong_pk(self):
        response = self.client.get(f'/api/v1/events/1564984984/')
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

    # filter check (list)
    def test_get_events_list_filtering_out_category(self):
        response = self.client.get('/api/v1/events/', query_params={"category": "concert"}) # filter logic was wrong
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        event = response.json()
        print(event)
        self.assertTrue(event['count'] == 1)
        self.assertEqual(event['results'][0]['name'], 'Ariana Grande Concert')


    # update
    def test_update_event_success(self):
        event = Event.objects.create(name='Awesome5', description='Awesome', category='play', open=True, start_at='2025-01-23', end_at='2025-01-23')
        user = User.objects.get(username='super')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.patch(f'/api/v1/events/{event.id}/', {
            "name": "Hisaishi Joe ghibli concert",
            "description": "Ghibli studio music",
            "category": "orchestra",
            "open": "true",
            "start_at": "2025-02-02",
            "end_at": "2025-02-04"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_event = response.json()
        self.assertEqual(updated_event['name'], "Hisaishi Joe ghibli concert")

    def test_update_event_not_found_fail(self):
        user = User.objects.get(username='super')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.patch('/api/v1/events/468468616/', {
            "name": "Hisaishi Joe ghibli concert",
            "description": "Ghibli studio music",
            "category": "orchestra",
            "open": "true",
            "start_at": "2025-02-02",
            "end_at": "2025-02-04"
        })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_admin_user_can_update_event(self):
        event = Event.objects.create(name='Awesome5', description='Awesome', category='play', open=True, start_at='2025-01-23', end_at='2025-01-23')
        user = User.objects.get(username='user1')
        self.client.force_login(user=user)

        response = self.client.patch(f'/api/v1/events/{event.id}/', {
            "name": "Hisaishi Joe ghibli concert",
            "description": "Ghibli studio music",
            "category": "orchestra",
            "open": "true",
            "start_at": "2025-02-02",
            "end_at": "2025-02-04"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # delete
    def test_delete_event_success(self):
        event = Event.objects.create(name='Awesome5', description='Awesome', category='play', open=True, start_at='2025-01-23', end_at='2025-01-23')
        user = User.objects.get(username='super')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(f'/api/v1/events/{event.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_not_found_fail(self):
        user = User.objects.get(username='super')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete('/api/v1/events/468468616/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_only_admin_user_can_delete_event(self):
        event = Event.objects.create(name='Awesome5', description='Awesome', category='play', open=True, start_at='2025-01-23', end_at='2025-01-23')
        user = User.objects.get(username='user1')
        self.client.force_login(user=user)

        response = self.client.delete(f'/api/v1/events/{event.id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)