from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from app import db

# Association table: many-to-many relationship between SkillSession and Skill
session_skill = db.Table('session_skill',
  Column('session_id', db.String(36), ForeignKey('skill_sessions.id'), primary_key=True),
  Column('skill_id', db.String(36), ForeignKey('skills.id'), primary_key=True)
)