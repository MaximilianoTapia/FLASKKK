from flask import render_template, redirect, session, request, flash
from flask_app import app


from flask_app.models.users import User
from flask_app.models.appointments import Appointment

@app.route('/new/appointment')
def new_appointment():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    return render_template('new_appointment.html', user=user)

@app.route("/create/appointment", methods=["POST"])
def create_appointment():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Appointment.valida_appointment(request.form):
        return redirect("/new/appointment")


    Appointment.save(request.form)
    return redirect("/dashboard")

@app.route("/edit/appointment/<int:id>")
def edit_appointment(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    data_appointment = {
        "id": id
    }
    appointment = Appointment.get_by_id(data_appointment)

    return render_template('edit_appointment.html', user=user, appointmente=appointment)

@app.route("/update/appointment", methods=["POST"])
def update_appointment():
    if 'user_id' not in session:
        return redirect('/')

    if not Appointment.valida_cita(request.form):
        return redirect("/edit/appointment/"+request.form['id'])
    
    Appointment.update(request.form)

    return redirect("/dashboard")

@app.route("/show/appointment/<int:id>")
def show_appointment(id):
    if 'user_id' not in session:
        return redirect('/')

    data_appointment = {
        "id": id
    }
    appointment = Appointment.get_by_id(data_appointment)

    return render_template("show_appointment.html", appointment=appointment)

@app.route("/delete/appointment/<int:id>")
def delete_appointment(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id":id
    }

    Appointment.delete(data)
    return redirect("/dashboard")
