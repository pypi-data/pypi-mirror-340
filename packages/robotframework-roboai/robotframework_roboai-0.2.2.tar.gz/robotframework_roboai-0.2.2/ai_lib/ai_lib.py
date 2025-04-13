import os
from openai import OpenAI
from dotenv import load_dotenv
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

load_dotenv()  # Load environment variables from .env

class AILibrary:

    def __init__(self, api_key=None  , model="gpt-4o"):
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("API key is required for AILibrary")
        
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def _get_driver(self):
        selib = BuiltIn().get_library_instance('SeleniumLibrary')
        return selib.driver
      
    
    @keyword("Ask Gpt")
    def ask_gpt(self , prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role" : "user" , "content" : prompt }]
        )
        return response.choices[0].message.content.strip()

    @keyword("Classify Text")    
    def classify_text(self, text):
        prompt = f"Classify the following message as either 'Issue' or 'OK':\n\n{text}"
        response = self.client.chat.completions.create(
            model= self.model,
            messages=[{"role" :"user" , "content" : prompt}]
        )
        return response.choices[0].message.content.strip()
    
    @keyword("Input Text in Other Language")
    def input_text_in_other_language(self , xpath , input_text , language):
        """
        Translate the input text to specified language and type into the element located by given xpath
        """ 
        prompt = f"Translate the following text to {language} :\n\n\"{input_text}\""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        translated_text = response.choices[0].message.content.strip()
        print(f"Translated text : {translated_text}")
        
        #  here get the driver and input translated text
        xpath_val = xpath
        driver = self._get_driver()
        if  'xpath:' in xpath:
            _, xpath_val =xpath.split('xpath:' , 1)
        try:
            element = driver.find_element(By.XPATH, xpath_val)
            element.clear()
            element.send_keys(translated_text)
        except NoSuchElementException:
            raise Exception(f"No such element found for xpath : {xpath_val}")
        
    @keyword("Extract XPath From Section Using AI")
    def extract_xpath_from_section_using_ai(self, parent_xpath, expected_section_description, expected_xpath_or_tag=None):
        """
        Extract the most accurate XPath of an element inside a section identified by parent_xpath,
        based on a natural language description of the expected element.

        Arguments:
        - parent_xpath: XPath to the larger surrounding section (<div>, etc.).
        - expected_section_description: A plain description of the element you're looking for.
        - expected_xpath_or_tag: Optional hint for element type or partial XPath (e.g., 'button', 'input[@type="submit"]').

        Returns:
        - A single XPath string for the desired element.
        """
        driver = self._get_driver()

        if 'xpath:' in parent_xpath:
            _, parent_xpath = parent_xpath.split('xpath:', 1)

        try:
            section_element = driver.find_element(By.XPATH, parent_xpath)
            section_html = section_element.get_attribute('outerHTML')
        except NoSuchElementException:
            raise Exception(f"Could not find section for parent_xpath: {parent_xpath}")

        prompt = f"""You are an expert in parsing HTML and crafting robust XPath expressions.

        Given the following HTML section:

        {section_html}

        Task:
        Based on the user’s goal and any available hints, return the most accurate and robust XPath for the element they want.

        Goal: {expected_section_description}
        Hint: {expected_xpath_or_tag if expected_xpath_or_tag else 'None'}

        Respond ONLY with the XPath string. Do NOT add any explanation or code formatting.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        output_xpath = response.choices[0].message.content.strip()
        print(f"AI returned XPath: {output_xpath}")
        return output_xpath