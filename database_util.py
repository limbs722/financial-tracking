from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://limbs:test!234@localhost:5432/trackingdb")
Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String)
    title = Column(String)
    source = Column(String)
    link = Column(String)
    __table_args__ = (UniqueConstraint("title", "link"),)


class JsonToDatabase:
    def __init__(self, data, ticker):
        self.data = data["data"]
        self.ticker = ticker

    def load(self):
        dry = False

        Session = sessionmaker(bind=engine)
        session = Session()

        # 테이블 확인 및 데이터 추가
        inspector = inspect(engine)
        if not inspector.has_table("news"):
            # 테이블 생성
            Base.metadata.create_all(engine)

        session.begin()

        try:
            for item in self.data:
                session.add(
                    News(
                        ticker=self.ticker,
                        title=item["title"],
                        source=item["source"],
                        link=item["link"],
                    )
                )

            if dry == False:
                session.commit()

        except Exception as e:
            print(str(e))
            session.rollback()

        finally:
            # 만약 session.close를 하지 않는다면?
            session.close()

        # with Session() as session:
        #     try:
        #         for item in self.data:
        #             session.add(
        #                 News(
        #                     title=item["title"],
        #                     source=item["source"],
        #                     link=item["link"],
        #                 )
        #             )

        #             if dry == False:
        #                 session.commit()
        #     except:
        #         print("Error")
        #         session.rollback()
