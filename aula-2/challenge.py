"""
 Observer Pattern Implementation in Python
 
 This module demonstrates the Observer design pattern, where a subject maintains a list of observers
 and notifies them of state changes.
 
 The Observer pattern is a behavioral design pattern that defines a one-to-many dependency between objects
 so that when one object changes state, all its dependents are notified and updated automatically.
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state
        self.notify()


class ConcreteObserverA(Observer):
    def update(self, subject):
        print(f"ConcreteObserverA: Reacted to the event. New state: {subject.state}")


class ConcreteObserverB(Observer):
    def update(self, subject):
        print(f"ConcreteObserverB: Reacted to the event. New state: {subject.state}")


if __name__ == "__main__":
    # Create a subject
    subject = Subject()
    
    # Create observers
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()
    
    # Register observers with the subject
    subject.attach(observer_a)
    subject.attach(observer_b)
    
    # Change the subject's state
    print("Changing subject state to 123...")
    subject.state = 123
    
    # Detach one observer
    subject.detach(observer_a)
    
    # Change the subject's state again
    print("\nChanging subject state to 456...")
    subject.state = 456