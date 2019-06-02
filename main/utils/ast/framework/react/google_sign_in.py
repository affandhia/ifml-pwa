from main.utils.ast.base import Node
from main.utils.ast.framework.react.components import \
    ReactComponentEseightClass
from main.utils.jinja.react import base_file_writer


class LoginClass(ReactComponentEseightClass):

    def __init__(self):
        super().__init__()
        self.selector_name = 'login'
        self.class_name = self.component_name = 'Login'

    def render(self):
        return base_file_writer('src/LoginPage/index.js.template')

    def get_class_name(self):
        return self.class_name


class LoginHTML(Node):

    def __init__(self):
        super().__init__()

    def render(self):
        return '''
<div>
  {this.props.isAuth && <Redirect to="/" />}
  <div>Input the Token here</div>
  <div>
    <textarea onChange={this.handleTokenChange} />
  </div>
  <div>- OR -</div>
  <div>
    <input
      onClick={this.handleLoginWithGoogle}
      value="Login with Google"
      type="button"
    />
    {/* <div id={GOOGLE_BUTTON_ID} /> */}
  </div>
</div>
        '''
