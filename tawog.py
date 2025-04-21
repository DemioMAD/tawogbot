from bs4 import BeautifulSoup
import requests

class Episode:
    def __init__(self, episode_name: str):
        self.episode_name = episode_name
        self.url = f"https://theamazingworldofgumball.fandom.com/wiki/{episode_name.replace(' ', '_')}"

    @property
    def synopsis(self):
        """
        The synopsis of the episode.
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            synopsis = soup.select("#content-1 > p")
            if not synopsis:
                return None
            
            if self.episode_name != "Early Reel":
                return synopsis[2].text
            else:
                return synopsis[3].text
        else:
            raise requests.RequestException(f"Response status code is other than 200. {response.status_code}")
        
    @property
    def info(self):
        """
        Information about the episode.
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            info = soup.select("#content-1 > p")
            if not info:
                return None

            return info[1].text.replace("[1]", "")
        else:
            raise requests.RequestException(f"Response status code is other than 200. {response.status_code}")
        
    @property
    def us_airdate(self):
        """
        The U.S. air date of the episode.
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            airdate = soup.select("section.pi-item:nth-child(5) > div:nth-child(2) > div:nth-child(2)")
            if not airdate:
                return None

            return airdate[0].text
        else:
            raise requests.RequestException(f"Response status code is other than 200. {response.status_code}")
        
    @property
    def uk_airdate(self):
        """
        The U.K. air date of the episode.
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            airdate = soup.select("section.pi-item:nth-child(5) > div:nth-child(3) > div:nth-child(2)")
            if not airdate:
                return None

            return airdate[0].text
        else:
            raise requests.RequestException(f"Response status code is other than 200. {response.status_code}")