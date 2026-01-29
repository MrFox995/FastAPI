# Here each model represent a Table of our DB
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Boolean, text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    ID = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

class Post(Base):
    __tablename__ = "posts"

    ID = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = True, server_default = 'TRUE')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    # The following code creates our FK constraints
    owner_ID = Column(Integer, ForeignKey("users.ID", ondelete = "CASCADE"), nullable = False)
    # sqlAlchemy Relationship
    owner = relationship("User")

class Vote(Base):
    __tablename__ = "votes"

    post_ID = Column(Integer, ForeignKey("posts.ID", ondelete = "CASCADE"), primary_key = True, nullable = False)
    user_ID = Column(Integer, ForeignKey("users.ID", ondelete = "CASCADE"), primary_key = True, nullable = False)


############################################## ALEMBIC TEST MODELS ##############################################
    
class UserTest(Base):
    __tablename__ = "users_test"

    ID = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

class PostTest(Base):
    __tablename__ = "posts_test"

    ID = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = True, server_default = 'TRUE')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    # The following code creates our FK constraints
    owner_ID = Column(Integer, ForeignKey("users_test.ID", ondelete = "CASCADE"), nullable = False)
    # sqlAlchemy Relationship
    owner = relationship("UserTest")

class VoteTest(Base):
    __tablename__ = "votes_test"

    post_ID = Column(Integer, ForeignKey("posts_test.ID", ondelete = "CASCADE"), primary_key = True, nullable = False)
    user_ID = Column(Integer, ForeignKey("users_test.ID", ondelete = "CASCADE"), primary_key = True, nullable = False)

############################################## ALEMBIC TEST MODELS ##############################################