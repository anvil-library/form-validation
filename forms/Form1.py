from anvil import *

import validation

class Form1(Form1Template):

  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # This is an example of how to validate a form
    self.validator = validation.Validator()
    self.validator.require_text_field(self.name_box, self.name_missing_lbl)
    self.validator.require(self.birthday_date, ['change'],
                           lambda date_picker: date_picker.date is not None,
                           self.birthday_missing_lbl)
    self.validator.require_checked(self.tos_accept_cbx, self.tos_missing_lbl)
    
    # Uncomment the line below to disable the button until the form is complete:
    #self.validator.enable_when_valid(self.submit_btn)

  def submit_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    if self.validator.is_valid():
      alert("Thanks for signing up")
    else:
      self.validator.show_all_errors()

