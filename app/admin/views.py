from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee

def check_admin():
    # Prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

@admin.route("/departments", methods=["GET", "POST"])
@login_required
def list_departments():
    # list all departments
    check_admin()

    departments = Department.query.all()

    return render_template("admin/departments/departments.html", departments=departments, title="Departments")

@admin.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
    check_admin()

    add_department = True

    form = DepartmentForm()

    if form.validate_on_submit():
        department = Department(
            name=form.name.data,
            description=form.description.data
        )

        try:
            # add department to db
            db.session.add(department)
            db.session.commit()
            flash("You have successfully added a new department")
        except:
            # in case department already exists
            flash("Error: department name already exists.")

        # redirect to departments page
        return redirect(url_for("admin.list_departments"))

    # load department template
    return render_template("admin/departments/department.html", action="Add", add_department=add_department, form=form, title="Add Department")

@admin.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash("You have successfully edited the department.")

        # redirect to departments page
        return redirect(url_for("admin.list_departments"))

    form.description.data = department.description
    form.name.data = department.name

    return render_template("admin/departments/department.html", action="Edit", add_department=add_department, form=form, department=department, title="Edit Department")

@admin.route("/departments/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_department(id):
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash("You have successfully deleted the department.")

    # redirecto to departments page
    return redirect(url_for("admin.list_departments"))

    return render_template(title="Delete Department")

@admin.route("/roles", methods=["GET", "POST"])
@login_required
def list_roles():
    # list all roles
    check_admin()

    roles = Role.query.all()

    return render_template("admin/roles/roles.html", roles=roles, title="Roles")

@admin.route("/roles/add", methods=["GET", "POST"])
@login_required
def add_role():
    check_admin()

    add_role = True

    form = RoleForm()

    if form.validate_on_submit():
        role = Role(
            name=form.name.data,
            description=form.description.data
        )

        try:
            # add department to db
            db.session.add(role)
            db.session.commit()
            flash("You have successfully added a new role.")
        except:
            # in case department already exists
            flash("Error: role name already exists.")

        # redirect to departments page
        return redirect(url_for("admin.list_roles"))

    # load department template
    return render_template("admin/roles/role.html", action="Add", add_role=add_role,form=form, title="Add Role")

@admin.route("/roles/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_role(id):
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.commit()
        flash("You have successfully edited the role.")

        # redirect to departments page
        return redirect(url_for("admin.list_roles"))

    form.description.data = role.description
    form.name.data = role.name

    return render_template("admin/roles/department.html", action="Edit", add_role=add_role, form=form, role=role, title="Edit Role")

@admin.route("/roles/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_role(id):
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash("You have successfully deleted the role.")

    # redirecto to departments page
    return redirect(url_for("admin.list_roles"))

    return render_template(title="Delete Role")

@admin.route("/employees", methods=["GET", "POST"])
@login_required
def list_employees():
    # list all departments
    check_admin()

    employees = Employee.query.all()

    return render_template("admin/employees/employees.html", employees=employees, title="Employees")

@admin.route("/employees/assing/<int:id>", methods=["GET", "POST"])
@login_required
def assign_employee(id):
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)

    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()

        flash("You have successfully assigned a department and role.")

        # redirect to the roles page
        return redirect(url_for("admin.list_employees"))

    return render_template("admin/employees/employee.html", employee=employee, form=form, title="Assign Employee")