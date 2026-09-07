"""Medical Knowledge Graph for entity relationships."""
import networkx as nx
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from typing import Optional

@dataclass
class MedicalEntity:
    id: str
    name: str
    entity_type: str  # symptom, condition, medication, body_part, procedure
    description: str
    synonyms: List[str]
    severity: Optional[str] = None  # mild, moderate, severe, critical

class MedicalKnowledgeGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.entities: Dict[str, MedicalEntity] = {}
        self._initialize_base_entities()
    
    def _initialize_base_entities(self):
        """Initialize with base medical entities."""
        base_entities = [
            # Symptoms
            MedicalEntity("symptom_chest_pain", "Chest Pain", "symptom", 
                         "Pain or discomfort in the chest area", 
                         ["chest discomfort", "chest tightness", "angina"], "moderate"),
            MedicalEntity("symptom_shortness_breath", "Shortness of Breath", "symptom",
                         "Difficulty breathing or feeling breathless",
                         ["dyspnea", "breathlessness", "can't breathe"], "moderate"),
            MedicalEntity("symptom_abdominal_pain", "Abdominal Pain", "symptom",
                         "Pain in the abdominal region",
                         ["stomach pain", "belly pain", "tummy ache"], "mild"),
            MedicalEntity("symptom_headache", "Headache", "symptom",
                         "Pain in the head or upper neck",
                         ["head pain", "migraine", "cephalalgia"], "mild"),
            MedicalEntity("symptom_fever", "Fever", "symptom",
                         "Elevated body temperature above normal",
                         ["high temperature", "pyrexia", "febrile"], "mild"),
            
            # Conditions
            MedicalEntity("condition_mi", "Myocardial Infarction", "condition",
                         "Heart attack - blockage of blood flow to heart muscle",
                         ["heart attack", "MI", "acute coronary syndrome"], "critical"),
            MedicalEntity("condition_pe", "Pulmonary Embolism", "condition",
                         "Blood clot in the lungs",
                         ["PE", "lung clot"], "critical"),
            MedicalEntity("condition_pneumonia", "Pneumonia", "condition",
                         "Infection of the lungs causing inflammation",
                         ["lung infection", "chest infection"], "moderate"),
            MedicalEntity("condition_appendicitis", "Appendicitis", "condition",
                         "Inflammation of the appendix",
                         ["appendix inflammation"], "moderate"),
            MedicalEntity("condition_migraine", "Migraine", "condition",
                         "Severe recurring headaches with other symptoms",
                         ["migraine headache"], "moderate"),
            
            # Body parts
            MedicalEntity("body_heart", "Heart", "body_part",
                         "Muscular organ that pumps blood through the circulatory system",
                         ["cardiac", "myocardium"]),
            MedicalEntity("body_lungs", "Lungs", "body_part",
                         "Pair of respiratory organs for gas exchange",
                         ["pulmonary", "respiratory system"]),
            MedicalEntity("body_abdomen", "Abdomen", "body_part",
                         "Body cavity containing digestive organs",
                         ["stomach area", "belly"]),
            MedicalEntity("body_head", "Head", "body_part",
                         "Upper part of the body containing brain, eyes, ears, nose, mouth",
                         ["cranial", "skull"]),
        ]
        
        for entity in base_entities:
            self.add_entity(entity)
        
        # Add relationships
        self._add_base_relationships()
    
    def _add_base_relationships(self):
        """Add base medical relationships."""
        relationships = [
            # Symptom -> Condition (symptom indicates condition)
            ("symptom_chest_pain", "condition_mi", "indicates", 0.9),
            ("symptom_chest_pain", "condition_pe", "indicates", 0.7),
            ("symptom_shortness_breath", "condition_pe", "indicates", 0.9),
            ("symptom_shortness_breath", "condition_pneumonia", "indicates", 0.7),
            ("symptom_abdominal_pain", "condition_appendicitis", "indicates", 0.8),
            ("symptom_headache", "condition_migraine", "indicates", 0.8),
            ("symptom_fever", "condition_pneumonia", "indicates", 0.6),
            ("symptom_fever", "condition_appendicitis", "indicates", 0.5),
            
            # Condition -> Body part (condition affects body part)
            ("condition_mi", "body_heart", "affects", 1.0),
            ("condition_pe", "body_lungs", "affects", 1.0),
            ("condition_pneumonia", "body_lungs", "affects", 1.0),
            ("condition_appendicitis", "body_abdomen", "affects", 1.0),
            ("condition_migraine", "body_head", "affects", 1.0),
            
            # Symptom -> Body part (symptom located in body part)
            ("symptom_chest_pain", "body_heart", "located_in", 0.8),
            ("symptom_chest_pain", "body_lungs", "located_in", 0.6),
            ("symptom_shortness_breath", "body_lungs", "located_in", 1.0),
            ("symptom_abdominal_pain", "body_abdomen", "located_in", 1.0),
            ("symptom_headache", "body_head", "located_in", 1.0),
        ]
        
        for source, target, rel_type, weight in relationships:
            if source in self.entities and target in self.entities:
                self.graph.add_edge(source, target, relation=rel_type, weight=weight)
    
    def add_entity(self, entity: MedicalEntity):
        """Add a medical entity to the graph."""
        self.entities[entity.id] = entity
        self.graph.add_node(entity.id, 
                           name=entity.name, 
                           type=entity.entity_type,
                           description=entity.description,
                           synonyms=entity.synonyms,
                           severity=entity.severity)
    
    def get_related_conditions(self, symptom_id: str, threshold: float = 0.5) -> List[Tuple[str, float]]:
        """Get conditions related to a symptom above threshold."""
        if symptom_id not in self.graph:
            return []
        
        related = []
        for neighbor in self.graph.neighbors(symptom_id):
            if self.entities[neighbor].entity_type == "condition":
                weight = self.graph[symptom_id][neighbor].get("weight", 0)
                if weight >= threshold:
                    related.append((neighbor, weight))
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    def get_related_body_parts(self, symptom_id: str) -> List[str]:
        """Get body parts related to a symptom."""
        if symptom_id not in self.graph:
            return []
        
        body_parts = []
        for neighbor in self.graph.neighbors(symptom_id):
            if self.entities[neighbor].entity_type == "body_part":
                body_parts.append(self.entities[neighbor].name)
        return body_parts
    
    def search_entities(self, query: str) -> List[MedicalEntity]:
        """Search entities by name or synonyms."""
        query_lower = query.lower()
        results = []
        for entity in self.entities.values():
            if (query_lower in entity.name.lower() or 
                any(query_lower in s.lower() for s in entity.synonyms)):
                results.append(entity)
        return results

# Singleton instance
medical_kg = MedicalKnowledgeGraph()
