from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://limbs:test!234@localhost:5432/trackingdb"
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String)
    title = db.Column(db.String)
    source = db.Column(db.String)
    link = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "title": self.title,
            "source": self.source,
            "link": self.link,
        }


@app.route("/news", methods=["GET"])
def get_news():
    news = News.query.all()
    news_list = [obj.to_dict() for obj in news]
    return jsonify(news_list)


if __name__ == "__main__":
    app.run()
