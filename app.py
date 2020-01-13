from flask import Flask,render_template, redirect
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:postgres@localhost/testdb')
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/today_events")
def today_events():
    d = datetime.date(datetime.now())
    return redirect("/events/" + str(d.year) + "/" + str(d.month) + "/" + str(d.day))


@app.route("/events/<int:year>/<int:month>/<int:day>")
def date_events(year, month, day):
    the_events = db.execute("SELECT * FROM events WHERE event_date_time::date = '" + str(year) + "-" + str(month)
                            + "-" + str(day) + "';").fetchall()
    if the_events is None:
        return "Sorry No events"
    
    print(the_events)
    return render_template("date_events.html", the_events=the_events)


if __name__ == '__main__':
    app.run(debug=True)