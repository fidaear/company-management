from flask import Flask, request, render_template_string
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

# Load the HTML forms
with open('project_form.html', 'r') as user_file:
    user_form_html = user_file.read()

with open('project_form.html', 'r') as project_file:
    project_form_html = project_file.read()

@app.route('/')
def home():
    return "Welcome to the Project Management System. Go to /project to submit a project."

@app.route('/project')
def project_form():
    return render_template_string(project_form_html)

@app.route('/submit_project', methods=['POST'])
def submit_project():
    # Extract form data
    identifiant = request.form['identifiant']

    name = request.form['name']

    duree_type = request.form['duree_type']

    duree = request.form['duree']

    taille = request.form['taille']

    num_employes = request.form['num_employes']
    
    description = request.form['description']

    # Check if idemp exists in users.xml
    if not os.path.exists('users.xml'):
        return "Error: users.xml does not exist. Please add users first."

    tree = ET.parse('users.xml')
    root = tree.getroot()



    

    # Check if projects.xml exists
    if os.path.exists('projects.xml'):
        project_tree = ET.parse('projects.xml')
        project_root = project_tree.getroot()
    else:
        project_root = ET.Element('projects')

    # Create a new project element
    project = ET.SubElement(project_root, 'project', identifiant=identifiant)

    ET.SubElement(project, 'name').text = name
    ET.SubElement(project, 'duree', {'type': duree_type}).text = duree
    ET.SubElement(project, 'taille', {'tailldeproject': taille}).text = f"{num_employes} employe"
    ET.SubElement(project, 'description').text = description

    # Write to the XML file
    project_tree = ET.ElementTree(project_root)
    project_tree.write('projects.xml', encoding='utf-8', xml_declaration=True)

    return "Project data submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
