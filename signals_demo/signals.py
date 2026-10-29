import threading
from django.dispatch import Signal, receiver
from .models import SignalRecord


assignment_signal = Signal()

observations = {
    "events": [],
    "caller_thread_id": None,
    "receiver_thread_id": None,
    "receiver_in_atomic_block": None,
    "created_record_id": None,
}

@receiver(assignment_signal)
def assignment_receiver(sender, message, **kwargs):
    observations["events"].append("receiver_started")
    observations["receiver_thread_id"] = threading.get_ident()
    observations["receiver_in_atomic_block"] = __import__(
        "django.db", fromlist=["connection"]
    ).connection.in_atomic_block

    record = SignalRecord.objects.create(message=message)
    observations["created_record_id"] = record.pk
    observations["events"].append("receiver_finished")
