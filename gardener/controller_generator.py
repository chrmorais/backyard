import os.path

from config import BASEDIR
from config import WHITE_SPACE

def generate_controller(model_name, model_components):
    model_name = model_name.lower()
    db_model_name = model_name.title()
    mod_counter = 1
    max_mod_index = len(model_components)
    controller_path = os.path.join(BASEDIR, 'app/controllers/'+model_name+'.py')
    
    controller_file = open(controller_path,'w')
    controller_file.write("from flask import Blueprint\n")
    controller_file.write("from flask import render_template\n")
    controller_file.write("from flask import json\n")
    controller_file.write("from flask import session\n")
    controller_file.write("from flask import url_for\n")
    controller_file.write("from flask import redirect\n")
    controller_file.write("from flask import request\n")
    controller_file.write("from flask import abort\n")
    controller_file.write("from flask import Response\n\n")
    controller_file.write("from datetime import datetime\n\n")
    controller_file.write("from app import db\n\n")
	
    # import related models
    controller_file.write("from app.models import " + db_model_name +"\n\n")

    # create blueprint
    controller_file.write(model_name+"_view = Blueprint('"+model_name+"_view', __name__)\n\n")

    controller_file.write("########### " + model_name + " REST controller ###########\n\n")
    controller_file.write("@"+model_name+"_view.route('/" + model_name + "',methods=['GET','POST'],defaults={'id':None})\n")
    controller_file.write("@"+model_name+"_view.route('/" + model_name + "/<id>',methods=['GET','PUT','DELETE'])\n")
    controller_file.write("def " + model_name + "_controller(id):\n")
    for component in model_components:
        controller_file.write(WHITE_SPACE + component['field_name'].lower() + " = request.values.get('" + component['field_name'].lower() + "')\n")
    controller_file.write("\n"+ WHITE_SPACE +"if id:\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "if request.method == 'GET':\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + model_name+" = "+model_name.title()+".query.get(id)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "if "+model_name+":\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + model_name+" = "+model_name+".dto()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return json.dumps(dict("+model_name+"="+model_name+"))\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return abort(404)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "elif request.method == 'PUT':\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + model_name + "_item = " + model_name.title() + ".query.get(id)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "if "+model_name+"_item:\n")
    for component in model_components:
        controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "if " + component['field_name'].lower() + ":" + model_name + "_item." + component['field_name'].lower() + " = " + component['field_name'].lower() + "\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + model_name + "_item.last_updated_on = datetime.now()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "db.session.add(" + model_name + "_item)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "db.session.commit()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return '', 204\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return abort(404)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "elif request.method == 'DELETE':\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + model_name + "_item = " + model_name.title() + ".query.get(id)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "if "+model_name+"_item:\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "db.session.delete(" + model_name + "_item)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "db.session.commit()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return '', 204\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return abort(404)\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "else:\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE +"return abort(405)\n")
    controller_file.write(WHITE_SPACE + "else:\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "if request.method == 'GET':\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + model_name + "_list = "+model_name.title()+".query.all()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "entries=None\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "if " + model_name + "_list:\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "entries = [" + model_name + ".dto() for " + model_name + " in " + model_name + "_list]\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return json.dumps(dict("+model_name+"=entries))\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "elif request.method == 'POST':\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "new_"+model_name+" = "+model_name.title()+"(\n")
    for component in model_components:
            controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + component['field_name'].lower() + ' = ' + component['field_name'].lower() + ',\n')
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "created_on = datetime.now(),\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "last_updated_on = datetime.now()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + ")\n\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "db.session.add(new_" + model_name + ")\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "db.session.commit()\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return json.dumps(dict("+model_name+"=new_"+model_name+".dto())), 201\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + "else:\n")
    controller_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + "return abort(405)\n\n")
    controller_file.close()

    main_path = os.path.join(BASEDIR, 'app/main.py')
    read_main_file = open(main_path, 'r')
    original_lines = read_main_file.readlines()
    ## import the blueprint file
    original_lines[16] = original_lines[16].strip()
    original_lines[16] = original_lines[16] + ', ' + model_name + '_view\n'
    
    
    main_file = open(main_path, 'w')

    for lines in original_lines:
        main_file.write(lines)
    main_file.close()

    main_file = open(main_path,'a')
    main_file.write("\napp.register_blueprint(" + model_name + "_view)")
    main_file.close()

    init_path = os.path.join(BASEDIR, 'app/controllers/__init__.py')
    init_file = open(init_path, 'a')
    init_file.write("\nfrom "+ model_name + " import "+model_name+ "_view")
    init_file.close()

    print "Tree REST controller generated"

def add_controller(controller_name):
    controller_name = controller_name.lower()
    controller_name = controller_name.replace(' ', '_')
    controller_name = controller_name.replace('\'', '_')
    controller_name = controller_name.replace('.', '_')
    controller_name = controller_name.replace(',', '_')
    controller_path = os.path.join(BASEDIR, "app/controllers/" + controller_name + ".py")

    controller_file = open(controller_path, 'w')
    controller_file.write("from flask import Blueprint\n")
    controller_file.write("from flask import render_template\n")
    controller_file.write("from flask import json\n")
    controller_file.write("from flask import session\n")
    controller_file.write("from flask import url_for\n")
    controller_file.write("from flask import redirect\n")
    controller_file.write("from flask import request\n")
    controller_file.write("from flask import abort\n")
    controller_file.write("from flask import Response\n\n")
    
    controller_file.write("from app import db\n\n")

    controller_file.write(controller_name + "_view = Blueprint('" + controller_name + "_view', __name__)\n\n")

    controller_file.write("@" + controller_name + "_view.route('/" + controller_name + "') #Link\n")
    controller_file.write("def " + controller_name + "_control():\n")
    controller_file.write(WHITE_SPACE + "# add your controller here\n")
    controller_file.write(WHITE_SPACE + "return \"controller stub\"")
    controller_file.close()

    main_path = os.path.join(BASEDIR, 'app/main.py')
    read_main_file = open(main_path, 'r')
    original_lines = read_main_file.readlines()

    ## import the blueprint file
    original_lines[16] = original_lines[2].strip()
    original_lines[16] = original_lines[2] + ', ' + controller_name + '_view\n'

    main_path = os.path.join(BASEDIR, 'app/main.py')
    main_file = open(main_path, 'w')

    for lines in original_lines:
        main_file.write(lines)
    main_file.close()

    main_file = open(main_path,'a')
    main_file.write("\napp.register_blueprint(" + controller_name + "_view)")
    main_file.close()

    init_path = os.path.join(BASEDIR, 'app/controllers/__init__.py')
    init_file = open(init_path, 'a')
    init_file.write("\nfrom "+ controller_name + " import " + controller_name + "_view")
    init_file.close()

    print '\nStub Controller generated\n'

# end of file