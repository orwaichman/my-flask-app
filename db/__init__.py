from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config
import db.models


engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

Session = scoped_session(sessionmaker(bind=engine))

models.Base.metadata.create_all(engine)
