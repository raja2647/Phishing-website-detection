from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScanResult(Base):
    __tablename__ = 'scan_results'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    url_length = Column(Integer)
    sha_hash = Column(String)
    is_https = Column(Boolean)
    domain = Column(String)
    contains_keywords = Column(Boolean)
    phishing_status = Column(String)
