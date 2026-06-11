from flask import Flask, render_template, request, redirect
from models import db, Ticket

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///support.db'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():

    if request.method == "POST":

        ticket = Ticket(
            title=request.form["title"],
            description=request.form["description"]
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect("/tickets")

    return render_template("create_ticket.html")

@app.route("/tickets")
def view_tickets():

    tickets = Ticket.query.all()

    return render_template(
        "tickets.html",
        tickets=tickets
    )

@app.route("/ticket/<int:id>")
def ticket_details(id):

    ticket = Ticket.query.get_or_404(id)

    return render_template(
        "ticket_details.html",
        ticket=ticket
    )

@app.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):

    ticket = Ticket.query.get_or_404(id)

    ticket.status = request.form["status"]

    db.session.commit()

    return redirect(f"/ticket/{id}")

@app.route("/delete-ticket/<int:id>", methods=["POST"])
def delete_ticket(id):

    ticket = Ticket.query.get_or_404(id)

    db.session.delete(ticket)
    db.session.commit()

    return redirect("/tickets")

if __name__ == "__main__":
    app.run(debug=True)