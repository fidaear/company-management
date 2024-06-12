from flask import Flask, request, redirect, url_for, render_template_string, flash
from lxml import etree as ET
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

# Load the HTML forms
with open('../employers/form.html', 'r') as user_file:
    user_form_html = user_file.read()

with open('../projects/project_form.html', 'r') as project_file:
    project_form_html = project_file.read()

with open('../employers/dashboard.html', 'r') as dashboard_file:
    dashboard_html = dashboard_file.read()

@app.route('/')
def home():
    return render_template_string(dashboard_html)

@app.route('/employee')
def employee_form():
    return render_template_string(user_form_html)

@app.route('/project')
def project_form():
    return render_template_string(project_form_html)

@app.route('/submit_employee', methods=['POST'])
def submit_employee():
    try:
        # Extract form data
        CIN = request.form['CIN']
        name = request.form['name']
        sexe = request.form['sexe']
        age = request.form['age']
        phone_type = request.form['phone_type']
        phone = request.form['phone']
        email = request.form['email']

        # Check if users.xml exists
        if os.path.exists('../employers/users.xml'):
            tree = ET.parse('../employers/users.xml')
            root = tree.getroot()
        else:
            root = ET.Element('Employers')

        # Create a new person element
        person = ET.SubElement(root, 'Persone')
        ET.SubElement(person, 'CIN').text = CIN
        ET.SubElement(person, 'name').text = name
        ET.SubElement(person, 'sexe', {'type': sexe})
        ET.SubElement(person, 'age').text = age
        ET.SubElement(person, 'phone', {'type': phone_type}).text = phone
        ET.SubElement(person, 'email').text = email

        # Write to the XML file
        tree = ET.ElementTree(root)
        tree.write('../employers/users.xml', encoding='utf-8', xml_declaration=True)

        flash('Employee data successfully saved!', 'success')
        return redirect(url_for('employee_form'))

    except Exception as e:
        flash(f'Error saving employee data: {str(e)}', 'danger')
        return redirect(url_for('employee_form'))

@app.route('/submit_project', methods=['POST'])
def submit_project():
    try:
        # Extract form data
        identifiant = request.form['identifiant']
        name = request.form['name']
        duree_type = request.form['duree_type']
        duree = request.form['duree']
        taille = request.form['taille']
        num_employes = request.form['num_employes']
        idemp = request.form['idemp']
        description = request.form['description']

        # Check if idemp exists in users.xml
        if not os.path.exists('../employers/users.xml'):
            flash("Error: users.xml does not exist. Please add users first.", 'danger')
            return redirect(url_for('project_form'))

        tree = ET.parse('../employers/users.xml')
        root = tree.getroot()

        # Find if the idemp exists in users.xml
        idemp_exists = any(person.find('CIN').text == idemp for person in root.findall('Persone'))

        if not idemp_exists:
            flash("Error: Employee ID (CIN) not found in users.xml.", 'danger')
            return redirect(url_for('project_form'))

        # Check if projects.xml exists
        if os.path.exists('../projects/projects.xml'):
            project_tree = ET.parse('../projects/projects.xml')
            project_root = project_tree.getroot()
        else:
            project_root = ET.Element('projects')

        # Create a new project element
        project = ET.SubElement(project_root, 'project', identifiant=identifiant)

        ET.SubElement(project, 'name').text = name
        ET.SubElement(project, 'duree', {'type': duree_type}).text = duree
        ET.SubElement(project, 'taille', {'tailldeproject': taille}).text = f"{num_employes} employe"
        ET.SubElement(project, 'idemp').text = idemp
        ET.SubElement(project, 'description').text = description

        # Write to the XML file
        project_tree = ET.ElementTree(project_root)
        project_tree.write('../projects/projects.xml', encoding='utf-8', xml_declaration=True)

        flash('Project data successfully saved!', 'success')
        return redirect(url_for('project_form'))

    except Exception as e:
        flash(f'Error saving project data: {str(e)}', 'danger')
        return redirect(url_for('project_form'))

@app.route('/display_employees')
def display_employees():
    try:
        # Load and transform XML with XSLT
        xml = ET.parse('../employers/users.xml')
        xslt = ET.parse('../employers/employees.xslt')
        transform = ET.XSLT(xslt)
        result = transform(xml)

        return render_template_string(str(result) + '''
            <br><a href="/employee" class="btn btn-secondary">Back to Employee Form</a>
        ''')
    except Exception as e:
        flash(f'Error displaying employee data: {str(e)}', 'danger')
        return redirect(url_for('home'))

@app.route('/display_projects')
def display_projects():
    try:
        # Load and transform XML with XSLT
        xml = ET.parse('../projects/projects.xml')
        xslt = ET.parse('../projects/projects.xslt')
        transform = ET.XSLT(xslt)
        result = transform(xml)

        return render_template_string(str(result) + '''
            <br><a href="/project" class="btn btn-secondary">Back to Project Form</a>
        ''')
    except Exception as e:
        flash(f'Error displaying project data: {str(e)}', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
