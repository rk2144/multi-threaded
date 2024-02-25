import queue
import threading
import concurrent.futures
import time

class Message:
    def __init__(self, content, priority):
        self.content = content
        self.priority = priority

class PriorityQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()

    def enqueue_message(self, message):
        self.queue.put((message.priority, message))

    def dequeue_message(self):
        if not self.is_empty():
            return self.queue.get()[1]

    def peek_message(self):
        if not self.is_empty():
            return self.queue.queue[0][1]

    def is_empty(self):
        return self.queue.empty()

class ThreadPool:
    def __init__(self, num_threads):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)

    def execute(self, func, *args):
        self.executor.submit(func, *args)

class ThreadMessaging:
    def __init__(self, thread_id, message_queue, thread_pool):
        self.thread_id = thread_id
        self.message_queue = message_queue
        self.thread_pool = thread_pool
        self.running = True

    def send_message(self, content, priority):
        message = Message(content, priority)
        self.message_queue.enqueue_message(message)
        print(f"Thread {self.thread_id} sent message: {content}")
        # Wake up receiver thread
        self.thread_pool.execute(self.receive_message)

    def receive_message(self):
        while self.running:
            if not self.message_queue.is_empty():
                message = self.message_queue.dequeue_message()
                print(f"Thread {self.thread_id} received message: {message.content}")
                self.thread_pool.execute(self.process_message, message)
            else:
                time.sleep(1)  # Sleep briefly if queue is empty

    def process_message(self, message):
        # Simulate processing
        print(f"Thread {self.thread_id} processing message: {message.content}")
        time.sleep(2)  # Simulate some processing time

def main():
    message_queue = PriorityQueue()
    thread_pool = ThreadPool(num_threads=3)  # 3 worker threads

    # Create threads
    threads = []
    for i in range(3):
        thread = ThreadMessaging(thread_id=i, message_queue=message_queue, thread_pool=thread_pool)
        threads.append(thread)
        threading.Thread(target=thread.receive_message).start()

    # Simulate sending messages
    for i in range(10):
        sender_id = i % 3  # Pick a sender thread
        priority = i % 3    # Varying priorities
        content = f"Message {i}"
        threads[sender_id].send_message(content, priority)

    # Let threads finish processing
    time.sleep(10)
    for thread in threads:
        thread.running = False

if __name__ == "__main__":
    main()
