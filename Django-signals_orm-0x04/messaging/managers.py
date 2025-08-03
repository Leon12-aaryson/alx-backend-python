from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager for filtering unread messages.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)
    
    def unread_for_user(self, user):
        """Filter unread messages for a specific user."""
        return self.filter(receiver=user).select_related('sender').only(
            'id', 'content', 'timestamp', 'sender__email', 'sender__first_name', 'sender__last_name'
        ) 