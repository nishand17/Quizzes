from jinja2 import Environment, FileSystemLoader, select_autoescape


templateLoader = FileSystemLoader( searchpath="./templates")
templateEnv = Environment( loader=templateLoader )
TEMPLATE_FILE = "index.html"
template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(name="Nishan") # this is where to put args to the template renderer

print(outputText)

