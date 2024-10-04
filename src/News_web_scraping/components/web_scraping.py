import time
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from News_web_scraping import logger
from News_web_scraping.utils.common import create_directories 
from News_web_scraping.config.configuration import ConfigurationManager
from News_web_scraping.pipeline.stage_02_prompt_and_chain import PromptAndChainPipeline



class WebPageScraper(ConfigurationManager):

    def __init__(self,URL):
        super().__init__()
        self.URL            = URL 
        self.soup           = None
        web_scraping_config = self.get_web_scraping_config()
        self.headers        = web_scraping_config.headers
        self.extract_file_path  = web_scraping_config.extracted_path


    def fetch_and_parse(self): 
        """Validate the URL, fetch the webpage, and parse the content using BeautifulSoup."""
        parsed_url = urlparse(self.URL)
        if not parsed_url.scheme:
            self.URL = f"http://{self.URL}"  
        
        try:
            response    = requests.get(self.URL, headers=self.headers)
            response.raise_for_status()  # Check for HTTP errors
            self.soup   = BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.MissingSchema:
            logger.error(f"Invalid URL: {self.URL} - Missing schema.")
            raise ValueError(f"Invalid URL: {self.URL} - Please provide a valid URL.")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while trying to reach {self.URL}.")
            raise ConnectionError(f"Failed to connect to {self.URL}.")
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error while trying to reach {self.URL}.")
            raise TimeoutError(f"Request to {self.URL} timed out.")
        
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error occurred: {err}")
            raise RuntimeError(f"HTTP error occurred: {err}")
        
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def clean_and_extract_text(self):
        """Remove unwanted tags and extract text from paragraph (<p>) tags."""
        if self.soup:
            for unwanted in self.soup(["script", "style", "a"]):
                unwanted.extract()
            paragraphs = self.soup.find_all('p')
            if paragraphs:
                return ' '.join(para.get_text(separator=' ', strip=True) for para in paragraphs)
            else:
                logger.warning("No paragraph tags found in the response.")
                return "No content found."
        return None
    


if __name__ == "__main__":
    #URL         = "https://medium.com/@hamedkazemi/breaking-the-token-limits-a-journey-with-chatgpt-langchain-and-vectordb-embeddings-bonus-32352f97f5d4"
    #URL  = "google.com"
    #URL = "https://indianexpress.com/article/explained/explained-global/why-chagos-islands-matter-why-uk-keeps-diego-garcia-base-9602682/?ref=newlist_hp"
    URL = "https://www.gsmarena.com/detailed_specs_for_samsungs_galaxy_a16_4g_and_5g_emerge-news-64767.php"
    scraper     = WebPageScraper(URL=URL)
    scraper.fetch_and_parse()
    page_text   = scraper.clean_and_extract_text()

    obj     = PromptAndChainPipeline()
    llm     = obj.main()

    print(llm.invoke(page_text))

    
