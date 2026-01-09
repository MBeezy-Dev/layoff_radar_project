from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self):
        """Muss eine Liste von Dictionaries zurückgeben"""
        pass
