from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


class SqlaSession:
    def __init__(self, s: Session) -> None:
        self.s: Session = s

    def execute(self, *args, **kwargs):
        return self.s.execute(text(args[0]), *args[1:], **kwargs)


@contextmanager
def S(url):
    if hasattr(url, "url"):
        url = url.url
    # an Engine, which the Session will use for connection
    # resources
    engine = create_engine(url)

    # create session and add objects
    with Session(engine) as session:
        yield SqlaSession(session)
        session.commit()
