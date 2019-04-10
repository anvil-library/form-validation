class Validator():
  """
A Validator instance performs form validation. You give it
a set of components, and for each component you specify
a checking function (a predicate), and optionally an error
label that will be shown if the component is *not* valid.

It will show error labels when the component is not valid

Add components to it with the require() method. Eg:

  validator.require(self.text_box_1, ['change', 'lost_focus'],
                    lambda tb: tb.text != '',
                    self.error_lbl_1)
                    
It also has some utility functions for common requirements
such as "this text box must have text in it", or
"this checkbox must be checked".

Use the enable_when_valid() method to provide a component
that will be enabled (via its `enable` property) only when
all requirements are met. Or just use the is_valid() method
to check the status of the form.

  validator.enable_when_valid(self.submit_button)

  """
  def __init__(self):
    self._validity = {}
    self._actions = []
    self._component_checks = []
    
  def require(self, component, event_list, predicate, error_lbl=None, show_errors_immediately=False):
    def check_this_component(**e):
      result = predicate(component)
      self._validity[component] = result
      if error_lbl is not None:
        error_lbl.visible = not result
      self._check()
      
    for e in event_list:
      component.set_event_handler(e, check_this_component)
    self._component_checks.append(check_this_component)
      
    if show_errors_immediately:
      check_this_component()
    else:
      # By default, won't show the error until the event triggers,
      # but we will (eg) disable buttons
      if error_lbl is not None:
        error_lbl.visible = False
      self._validity[component] = predicate(component)
      self._check()
   
  def require_text_field(self, text_box, error_lbl=None, show_errors_immediately=False):
    self.require(text_box, ['change', 'lost_focus'],
                 lambda tb: tb.text not in ('', None),
                 error_lbl, show_errors_immediately)
        
  def require_checked(self, check_box, error_lbl=None, show_errors_immediately=False):
    self.require(check_box, ['change'],
                 lambda cb: cb.checked,
                 error_lbl, show_errors_immediately)
      
  def enable_when_valid(self, component):
    def on_change(is_valid):
      component.enabled = is_valid
    self._actions.append(on_change)
    self._check()

  def is_valid(self):
    """Return True if this form is valid, False if it's not."""
    return all(self._validity.values())
  
  def show_all_errors(self):
    """Run all component checks and perform the appropriate actions if any fields are invalid."""
    for check_component in self._component_checks:
      check_component()
    
  def _check(self):
    v = self.is_valid()
    for f in self._actions:
      f(v)
