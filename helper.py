from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver', options=chrome_options)


class BBC:
    def __init__(self, url:str,headerClass:str,editorClass:str,bodyClass:str):
      wd.get(url)
      self.header=self.get_header(headerClass)
      self.editor=self.get_editor(editorClass)
      self.articleBody=self.get_articlebody(bodyClass)

    #returns header 
    def get_header(self,headerClass) -> list:
      return wd.find_elements_by_class_name(headerClass)
      
    #returns editor
    def get_editor(self,editorClass) -> list:
      if wd.find_elements_by_class_name(editorClass):
        return wd.find_elements_by_class_name(editorClass)[0].text
      else:
        return ''

    #returns article body
    def get_articlebody(self,bodyClass) -> list:
      return wd.find_elements_by_class_name(bodyClass)
