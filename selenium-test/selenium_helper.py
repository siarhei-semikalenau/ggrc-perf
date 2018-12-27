class element_text_has_changed(object):

  def __init__(self, locator, text):
    self.locator = locator
    self.text = text

  def __call__(self, driver):
    element = driver.find_element(*self.locator)
    if (element.text == self.text):
      return False
    else:
      return element

class elements_number_has_changed(object):

  def __init__(self, locator, number):
    self.locator = locator
    self.number = number

  def __call__(self, driver):
    elements = driver.find_elements(*self.locator)
    if (len(elements) == self.number):
      return False
    else:
      return elements
