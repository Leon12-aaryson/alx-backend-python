from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory, Conversation


class MessagingModelsTestCase(TestCase):
    """Test case for messaging models functionality."""
    
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role='guest'
        )
        self.user2 = self.User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith',
            role='host'
        )

    def test_user_creation(self):
        """Test user model creation and fields."""
        self.assertEqual(self.user1.email, 'user1@test.com')
        self.assertEqual(self.user1.get_full_name(), 'John Doe')
        self.assertEqual(self.user1.role, 'guest')
        self.assertTrue(self.user1.is_active)

    def test_message_creation(self):
        """Test message model creation."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, this is a test message!'
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Hello, this is a test message!')
        self.assertFalse(message.edited)
        self.assertFalse(message.is_read)

    def test_notification_creation(self):
        """Test notification model creation."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message for notification'
        )
        notification = Notification.objects.create(
            user=self.user2,
            message=message,
            notification_type='new_message',
            title='New message received',
            content='You have received a new message'
        )
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'new_message')
        self.assertFalse(notification.is_read)

    def test_message_history_creation(self):
        """Test message history model creation."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original message content'
        )
        history = MessageHistory.objects.create(
            message=message,
            old_content='Previous content',
            edited_by=self.user1,
            edit_reason='Typo correction'
        )
        self.assertEqual(history.message, message)
        self.assertEqual(history.old_content, 'Previous content')
        self.assertEqual(history.edited_by, self.user1)
        self.assertEqual(history.edit_reason, 'Typo correction')


class MessagingSignalsTestCase(TestCase):
    """Test case for messaging signals functionality."""
    
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role='guest'
        )
        self.user2 = self.User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith',
            role='host'
        )

    def test_message_notification_signal(self):
        """Test that notification is created when message is created."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, this is a test message!'
        )
        notifications = Notification.objects.filter(
            user=self.user2,
            message=message,
            notification_type='new_message'
        )
        self.assertEqual(notifications.count(), 1)
        notification = notifications.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'new_message')

    def test_message_edit_history_signal(self):
        """Test that message history is created when message is edited."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original message content'
        )
        message.content = 'Updated message content'
        message.save()
        history_entries = MessageHistory.objects.filter(message=message)
        self.assertEqual(history_entries.count(), 1)
        history = history_entries.first()
        self.assertEqual(history.old_content, 'Original message content')
        self.assertEqual(history.edited_by, self.user1)
        message.refresh_from_db()
        self.assertTrue(message.edited)
        self.assertIsNotNone(message.edited_at)

    def test_message_edit_notification_signal(self):
        """Test that notification is created when message is edited."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original message content'
        )
        Notification.objects.all().delete()
        message.content = 'Updated message content'
        message.save()
        edit_notifications = Notification.objects.filter(
            user=self.user2,
            message=message,
            notification_type='message_edited'
        )
        self.assertEqual(edit_notifications.count(), 1)


class MessagingORMTestsCase(TestCase):
    """Test case for advanced ORM operations and queries."""
    
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role='guest'
        )
        self.user2 = self.User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith',
            role='host'
        )
        self.message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='First message from user1 to user2'
        )
        self.message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply from user2 to user1'
        )

    def test_select_related_optimization(self):
        """Test select_related for foreign key optimization."""
        messages = Message.objects.all()
        messages_optimized = Message.objects.select_related('sender', 'receiver').all()
        self.assertEqual(messages.count(), messages_optimized.count())

    def test_annotate_aggregation(self):
        """Test annotate for aggregations."""
        from django.db.models import Count
        users_with_message_count = self.User.objects.annotate(
            sent_count=Count('sent_messages'),
            received_count=Count('received_messages')
        )
        user1_data = users_with_message_count.get(email='user1@test.com')
        self.assertEqual(user1_data.sent_count, 1)
        self.assertEqual(user1_data.received_count, 1)

    def test_complex_queries_with_q_objects(self):
        """Test complex queries using Q objects."""
        from django.db.models import Q
        messages = Message.objects.filter(
            Q(sender=self.user1) | Q(receiver=self.user2)
        )
        self.assertEqual(messages.count(), 2)
        messages = Message.objects.filter(
            Q(sender=self.user1) & Q(receiver=self.user2)
        )
        self.assertEqual(messages.count(), 1)
