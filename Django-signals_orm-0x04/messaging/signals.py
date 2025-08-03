from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory, User


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create a notification when a new message is created.
    
    This signal listens for new Message instances and creates a notification
    for the receiving user to inform them about the new message.
    """
    if created:
        # Create notification for the receiver
        notification = Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='new_message',
            title=f"New message from {instance.sender.get_full_name() or instance.sender.email}",
            content=f"You received a new message: {instance.content[:100]}{'...' if len(instance.content) > 100 else ''}"
        )
        
        # Log the notification creation (optional)
        print(f"Notification created for {instance.receiver.email}: {notification.title}")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits before saving the updated message.
    
    This signal captures the old content of a message before it's updated
    and stores it in the MessageHistory model for tracking purposes.
    """
    if instance.pk:  # Only for existing messages (not new ones)
        try:
            # Get the old message from database
            old_message = Message.objects.get(pk=instance.pk)
            
            # Check if content has changed
            if old_message.content != instance.content:
                # Create history entry with old content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender,  # Assuming the sender is editing
                    edit_reason="Message content updated"
                )
                
                # Mark message as edited
                instance.edited = True
                instance.edited_at = timezone.now()
                
                # Create notification for message edit
                Notification.objects.create(
                    user=instance.receiver,
                    message=instance,
                    notification_type='message_edited',
                    title=f"Message edited by {instance.sender.get_full_name() or instance.sender.email}",
                    content=f"A message sent to you has been edited."
                )
                
                print(f"Message edit logged for message {instance.id}")
                
        except Message.DoesNotExist:
            # This shouldn't happen in normal flow, but handle gracefully
            print(f"Warning: Could not find original message {instance.pk} for edit logging")


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to automatically clean up user-related data when a user is deleted.
    
    This signal ensures that all messages, notifications, and message histories
    associated with the deleted user are properly cleaned up.
    """
    # Note: Due to CASCADE delete, most of this will be handled automatically
    # But we can add custom cleanup logic here if needed
    
    print(f"User {instance.email} deleted. Cleaning up related data...")
    
    # Additional cleanup can be added here if needed
    # For example, logging the deletion, sending notifications to other users, etc.


@receiver(post_save, sender=Message)
def update_message_read_status(sender, instance, **kwargs):
    """
    Signal to handle message read status updates.
    
    This signal can be used to automatically mark messages as read
    when certain conditions are met (e.g., user views the message).
    """
    # This is a placeholder for future functionality
    # You can implement logic here to automatically mark messages as read
    # based on user actions or other criteria
    pass


@receiver(post_save, sender=Notification)
def log_notification_creation(sender, instance, created, **kwargs):
    """
    Signal to log notification creation for debugging and monitoring.
    """
    if created:
        print(f"Notification created: {instance.notification_type} for {instance.user.email}")


# Signal to handle message deletion (if needed)
@receiver(post_delete, sender=Message)
def handle_message_deletion_notification(sender, instance, **kwargs):
    """
    Signal to handle notifications when messages are deleted.
    """
    # Create notification for message deletion
    try:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='message_deleted',
            title=f"Message deleted by {instance.sender.get_full_name() or instance.sender.email}",
            content=f"A message sent to you has been deleted."
        )
        print(f"Message deletion notification created for {instance.receiver.email}")
    except:
        # Handle case where user might have been deleted
        print(f"Could not create deletion notification for message {instance.id}") 