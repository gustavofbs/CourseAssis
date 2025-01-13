from abc import ABC, abstractmethod

class UserDataCollector(ABC):
    def collect_data(self):
        """Template method that defines the algorithm's skeleton."""
        self.collect_name()
        self.collect_interests()
        self.collect_experience_level()
        return self.get_user_data()
    
    @abstractmethod
    def collect_name(self):
        pass
    
    @abstractmethod
    def collect_interests(self):
        pass
    
    @abstractmethod
    def collect_experience_level(self):
        pass
    
    @abstractmethod
    def get_user_data(self):
        pass

class WebUserDataCollector(UserDataCollector):
    def __init__(self):
        self.user_data = {
            "name": "",
            "interests": [],
            "experience_level": ""
        }
    
    def collect_name(self):
        # Will be collected via web form
        pass
    
    def collect_interests(self):
        # Will be collected via web form
        pass
    
    def collect_experience_level(self):
        # Will be collected via web form
        pass
    
    def get_user_data(self):
        return self.user_data
