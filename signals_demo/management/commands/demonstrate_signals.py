import threading
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from signals_demo.models import SignalRecord
from signals_demo.signals import assignment_signal, observations

class Command(BaseCommand):
    help = "Demonstrate Django signal execution, thread, and transaction behavior."

    def handle(self, *args, **options):
        observations["events"] = []
        observations["caller_thread_id"] = threading.get_ident()
        observations["receiver_thread_id"] = None
        observations["receiver_in_atomic_block"] = None
        observations["created_record_id"] = None

        self.stdout.write("\nQUESTION 1: Synchronous or asynchronous?")
        observations["events"].append("caller_before_send")
        self.stdout.write("Caller: before send()")
        assignment_signal.send(sender=self.__class__, message="synchronous demo")
        observations["events"].append("caller_after_send")
        self.stdout.write("Caller: after send()")
        self.stdout.write("Observed order: " + " -> ".join(observations["events"]))
        self.stdout.write(
            "Conclusion: receiver_started and receiver_finished occur before "
            "caller_after_send, so send() is synchronous by default."
        )

        self.stdout.write("\nQUESTION 2: Same thread?")
        self.stdout.write(f"Caller thread ID:   {observations['caller_thread_id']}")
        self.stdout.write(f"Receiver thread ID: {observations['receiver_thread_id']}")
        self.stdout.write(
            "Conclusion: IDs match = "
            f"{observations['caller_thread_id'] == observations['receiver_thread_id']}"
        )

        self.stdout.write("\nQUESTION 3: Same database transaction?")
        before_count = SignalRecord.objects.count()
        try:
            with transaction.atomic():
                assignment_signal.send(
                    sender=self.__class__, message="transaction rollback demo"
                )
                self.stdout.write(
                    f"Receiver sees connection.in_atomic_block = "
                    f"{observations['receiver_in_atomic_block']}"
                )
                self.stdout.write(
                    f"Record count inside atomic block: {SignalRecord.objects.count()}"
                )
                raise RuntimeError("Intentional rollback for demonstration")
        except RuntimeError:
            self.stdout.write("Caller forced transaction rollback.")

        after_count = SignalRecord.objects.count()
        self.stdout.write(f"Record count before: {before_count}")
        self.stdout.write(f"Record count after:  {after_count}")
        self.stdout.write(
            "Conclusion: the receiver's write was rolled back with the caller's "
            "atomic transaction."
        )
        self.stdout.write(
            "\nNote: signals do not create transactions themselves. This example "
            "uses transaction.atomic() to demonstrate shared transaction behavior."
        )
