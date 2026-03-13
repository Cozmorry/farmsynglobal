# backend/modules/agronomy/models.py
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import JSON


# ============================================================
# AGRONOMY RECOMMENDATIONS
# ============================================================

class AgronomyRecommendation(Base):
    __tablename__ = "agronomy_recommendations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, nullable=False)  # Added to match schema and reports
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)

    recommendation_text = Column(Text, nullable=False)
    recommended_action = Column(String(255), nullable=True)
    date_given = Column(Date, default=datetime.date.today)
    generated_by = Column(String(255), nullable=True)
    source = Column(String(255), nullable=True)
    priority = Column(String(255), nullable=True)
    status = Column(String(255), default="Pending")

    crop = relationship("Crop", back_populates="agronomy_recommendations")
    block = relationship("Block")
    uploads = relationship("AgronomyUpload", back_populates="recommendation", cascade="all, delete-orphan")


class AgronomyUpload(Base):
    __tablename__ = "agronomy_uploads"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("agronomy_recommendations.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text, nullable=True)

    recommendation = relationship("AgronomyRecommendation", back_populates="uploads")


class AgronomyObservation(Base):
    __tablename__ = "agronomy_observations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)
    observation_date = Column(Date, default=datetime.date.today)
    notes = Column(Text, nullable=False)
    pest_issues = Column(Text, nullable=True)
    disease_issues = Column(Text, nullable=True)
    nutrient_deficiencies = Column(Text, nullable=True)
    suggested_action = Column(Text, nullable=True)
    reported_by = Column(String(255), nullable=True)

    crop = relationship("Crop")
    block = relationship("Block")
    uploads = relationship("AgronomyObservationUpload", back_populates="observation", cascade="all, delete-orphan")


class AgronomyObservationUpload(Base):
    __tablename__ = "agronomy_observation_uploads"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    observation_id = Column(Integer, ForeignKey("agronomy_observations.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text, nullable=True)

    observation = relationship("AgronomyObservation", back_populates="uploads")

