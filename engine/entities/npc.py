#npc.py
from saves.utilities.entity import Entity
class NPC(Entity):
    """
    Clase para representar a un NPC (personaje no jugador) en el juego.
    Hereda de la clase base Entity y puede tener comportamientos y atributos adicionales.
    """
    def __init__(self, name, race, stats, role):
        super().__init__(name, race, stats)
        self.role = role  # Rol del NPC (e.g., "merchant", "guard", "quest_giver")

        self.personality = {}     # Rasgos de personalidad (para NPCs)



    def add_personality_trait(self, trait_name, trait_value):
        """
        Agrega un rasgo de personalidad a la entidad (relevante para NPCs).
        """
        self.personality[trait_name] = trait_value
        