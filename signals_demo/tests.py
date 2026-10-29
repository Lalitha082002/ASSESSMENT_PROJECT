import threading
from django.db import connection, transaction
from django.test import TestCase
from .models import SignalRecord
from .rectangle import Rectangle
from .signals import assignment_signal, observations

class DjangoSignalsAssignmentTests(TestCase):
    def setUp(self):
        observations["events"] = []
        observations["caller_thread_id"] = None
        observations["receiver_thread_id"] = None
        observations["receiver_in_atomic_block"] = None
        observations["created_record_id"] = None

    def test_signal_receiver_runs_synchronously(self):
    
        
        observations["events"].append("caller_before_send")
        assignment_signal.send(sender=self.__class__, message="sync test")
        observations["events"].append("caller_after_send")

        self.assertEqual(
            observations["events"],
            [
                "caller_before_send",
                "receiver_started",
                "receiver_finished",
                "caller_after_send",
            ],
        )

    def test_signal_receiver_runs_in_same_thread(self):
        caller_thread_id = threading.get_ident()
        assignment_signal.send(sender=self.__class__, message="thread test")
        receiver_thread_id = observations["receiver_thread_id"]

        self.assertEqual(receiver_thread_id, caller_thread_id)

    def test_receiver_database_write_uses_callers_atomic_transaction(self):
        
        before_count = SignalRecord.objects.count()
        try:
            with transaction.atomic():
                assignment_signal.send(
                    sender=self.__class__, message="must roll back"
                )
                self.assertTrue(observations["receiver_in_atomic_block"])
                self.assertEqual(SignalRecord.objects.count(), before_count + 1)
                raise RuntimeError("force rollback")
        except RuntimeError:
            pass

        self.assertEqual(SignalRecord.objects.count(), before_count)

class RectangleTests(TestCase):
    def test_iteration_yields_length_then_width(self):
        rectangle = Rectangle(10, 5)
        self.assertEqual(list(rectangle), [{"length": 10}, {"width": 5}])

    def test_non_integer_values_are_rejected(self):
        with self.assertRaises(TypeError):
            Rectangle("10", 5)
