class Entity:
    """
    Clase base para representar cualquier entidad del juego (jugador o NPC).
    Contiene stats, habilidades, inventario, estado de salud y otros atributos.
    """
    
    def __init__(self, name, new_stats, height):
        # Información básica
        self.name = name
        self.race = {}          # Puede ser híbrido: {"orc":50, "human":50}
        self.stats = new_stats
        

        # Habilidades y rasgos
        self.skills = {}          # Skills y niveles
        self.holded_skills_experience = {}  # Experiencia de habilidades acumulada
        self.abilities = {}       # Habilidades activables
        self.magic = {}           # Habilidades mágicas
        self.magic_domain = {}    # Dominios mágicos del personaje
        self.magic_heat = 0       # Define cuantas veces puedes usar hechizos antes de sobrecalentar 
                                  # tus capacidades magicas e inivir las mismas
        self.max_magic_heat = 100   # Calor mágico máximo permitido
        self.holded_magic_experience = {}  # Experiencia mágica acumulada

        
        #Atributos Mundanos
        self.age = 0               # Edad inicial de la entidad
        self.hunger = 100          # Nivel de hambre
        self.thirst = 100          # Nivel de sed
        self.tiredness = 100       # Nivel de cansancio
        self.weight = 80            # Peso total de la entidad en kilogramos
        self.height = height        # Altura total de la entidad en centímetros
        self.inventory_weight_limit = (((self.stats["strength"] * 3) + (self.stats["constitution"]) * 2))  # Límite de peso del inventario en kilogramos
        self.inventory_weight = 0  # Límite de peso del inventario en kilogramos
        self.reputation = 0        # Reputación de la entidad
        self.state = "conscious"  # "conscious", "knocked_out", "Sleep", "poisoned", "dead" and so on
        self.family = []           # Lista de miembros de la familia (para interacciones y relaciones)
    

        # Inventario y quests
        self.inventory = []       # Objetos que posee la entidad
        self.equipped = {
            "main": None,
            "offhand": None,
            "head": None,
            "neck": None,
            #Superior
            #Brazo izquierdo
            "left_shoulder": None,
            "left_arm": None,
            "left_hand": None,
            "left_thumb": None,
            "left_index": None,
            "left_middle": None,
            "left_ring": None,
            "left_pinky": None,

            #Brazo derecho
            "right_shoulder": None,
            "right_arm": None,
            "right_hand": None,
            "right_thumb": None,
            "right_index": None,
            "right_middle": None,
            "right_ring": None,
            "right_pinky": None,

            #Torso
            "chest": None,
            "abdomen": None,
            "waist": None,

            #Inferior
            #Pierna izquierda
            "left_leg": None,
            "left_ankle": None,
            "left_foot": None,

            #Pierna derecha
            "right_leg": None,
            "right_ankle": None,
            "right_foot": None,

        }        # Objetos equipados (armas, armaduras, accesorios)
        self.quests = {}          # Quests activas
        
        # Atributos de combate y supervivencia
        self.level = 1
        self.experience = 0
        self.experience_modifier = 1.0
        self.max_health = ((self.stats["constitution"] * 2) + self.stats["strength"] + (self.weight * self.height)/2)
        self.current_health = self.max_health
        self.max_mana = ((self.stats["intellect"] * 3) + (self.stats["education"]) + (self.stats["will"] * 2) + (self.stats["psique"] * 2))/2
        self.current_mana = self.max_mana
        self.stamina = self.stats["constitution"] * 5 + (self.stats["agility"] + self.stats["dexterity"]) * 2  # Stamina inicial basada en constitución y agilidad
        

    

    # ------------------------------
    # Métodos de combate y habilidades
    # ------------------------------
    
    def take_damage(self, amount):
        """
        Reduce la salud de la entidad y actualiza su estado.
        """
        self.current_health -= amount
        
        if self.current_health <= 0:
            if self.current_health <= -self.max_health // 2:
                self.change_state("dead")
            else:
                self.change_state("knocked_out")


    
    def use_ability(self, ability_name, target):
        """
        Ejecuta una habilidad si la entidad la posee.
        """
        if ability_name in self.abilities:
            self.abilities[ability_name](self, target)
        else:
            print(f"Ability {ability_name} not found.")
    
    def add_ability(self, ability_name, ability_function):
        """
        Agrega una habilidad a la entidad.
        """
        self.abilities[ability_name] = ability_function
    
    def use_mana(self, mana, heat):
        """
        Consume mana si hay suficiente disponible.
        """
        if self.current_mana >= mana and self.magic_heat + heat <= self.max_magic_heat:
            self.current_mana -= mana
            self.magic_heat += heat
        else:
            print("Not enough mana or max magic heat reached.")

    # ------------------------------
    # Métodos de restauración
    # ------------------------------
    
    def restore_health(self, amount):
        """
        Restaura salud hasta el máximo permitido.
        """
        if self.state != "knocked_out":
            self.current_health += amount
            if self.current_health > self.max_health:
                self.current_health = self.max_health
        else:
            print("Entity is knocked out and cannot be self-healed.")
    
    def restore_mana(self, amount):
        """
        Restaura mana hasta el máximo permitido.
        """
        if self.state != "knocked_out":
            self.current_mana += amount
            if self.current_mana > self.max_mana:
                self.current_mana = self.max_mana
        else:
            print("Entity is knocked out and cannot be self-healed.")
    
    def alter_stamina(self, amount):
        """
        Modifica stamina de forma positiva o negativa, manteniéndola entre 0 y 100.
        """
        self.stamina += amount
        if self.stamina > 100:
            self.stamina = 100
        elif self.stamina < 0:
            self.stamina = 0
    
    
    
    
    
    
    # ------------------------------
    # Métodos de inventario y quests
    # ------------------------------

    def add_to_inventory(self, item, weight):
        self.inventory.append(item)
        self.weight += weight

    def remove_from_inventory(self, item, weight):
        if item in self.inventory:
            self.inventory.remove(item)
            self.weight -= weight

    def add_quest(self, quest_name, quest_details):
        self.quests[quest_name] = quest_details
    
    def remove_quest(self, quest_name):
        if quest_name in self.quests:
            del self.quests[quest_name]
    
   
   

   
   
   
    # ------------------------------
    # Métodos de magia y skills
    # ------------------------------
    
    def add_skill(self, skill_name):
        """
        Agrega o modifica una skill de la entidad.
        """
        self.skills[skill_name] = {"level": 1, "experience": 0, "efficiency": 1.0}
    
    def add_magic_skill(self, magic_name):
        """
        Agrega o modifica una habilidad mágica de la entidad.
        """
        self.magic[magic_name] = {"level": 1, "experience": 0, "efficiency": 1.0}

    def add_magic_domain(self, domain_name, domain_value):
        """
        Agrega o modifica un dominio mágico de la entidad.
        """
        self.magic_domain[domain_name] = domain_value

    def add_holded_magic_experience(self, amount, magic_name):
        """
        Agrega experiencia mágica a la entidad.
        """
        if magic_name not in self.holded_magic_experience:
            self.holded_magic_experience[magic_name] = 0
        self.holded_magic_experience[magic_name] += amount

    def add_holded_skill_experience(self, amount, skill_name):
        """
        Agrega experiencia de habilidad a la entidad.
        """
        if skill_name not in self.holded_skills_experience:
            self.holded_skills_experience[skill_name] = 0
        self.holded_skills_experience[skill_name] += amount

    def _threshold(self, level, base_xp=500, growth=1.1):
        """
        Calcula la experiencia necesaria para subir de nivel.
        Se escala en un 10% más que el nivel anterior.
        """
        return base_xp * (growth ** (level - 1))

    def apply_experience(self):
        """
        Aplica toda la experiencia retenida en magia y habilidades,
        convirtiéndola en niveles, experiencia y eficiencia.
        """
        self._process_experience(self.magic, self.holded_magic_experience)
        self._process_experience(self.skills, self.holded_skills_experience)


    def _process_experience(self, source_dict, exp_buffer):
        """
        Procesa experiencia de un diccionario de habilidades o magias.
        
        source_dict: diccionario del personaje (self.magic o self.skills)
        exp_buffer: diccionario temporal (self.holded_magic_experience o self.holded_skills_experience)
        """
        for name, exp in exp_buffer.items():
            # Inicializar si no existe
            if name not in source_dict:
                source_dict[name] = {"level": 1, "experience": 0, "efficiency": 1.0}

            data = source_dict[name]
            data["experience"] += exp  # sumamos lo acumulado
            exp_buffer[name] = 0       # vaciar buffer

            # Aplicar subida de nivel
            threshold = self._threshold(data["level"])
            while data["experience"] >= threshold:
                data["experience"] -= threshold
                data["level"] += 1
                data["efficiency"] += 0.01
                threshold = self._threshold(data["level"])

   
   
   
   
   
    # ------------------------------
    # Métodos de atributos mundanos
    # ------------------------------

    def add_family_member(self, member_entity, relation):
        if not any(f["entity"] == member_entity for f in self.family):
            self.family.append({"entity": member_entity, "relation": relation})


    def alter_hunger(self, amount):
        """
        Modifica el nivel de hambre de la entidad.
        """
        self.hunger += amount
        if self.hunger > 100:
            self.hunger = 100
        elif self.hunger < 0:
            self.hunger = 0

    def alter_thirst(self, amount):
        """
        Modifica el nivel de sed de la entidad.
        """
        self.thirst += amount
        if self.thirst > 100:
            self.thirst = 100
        elif self.thirst < 0:
            self.thirst = 0

    def alter_tiredness(self, amount):
        """
        Modifica el nivel de cansancio de la entidad.
        """
        self.tiredness += amount
        if self.tiredness > 100:
            self.tiredness = 100
        elif self.tiredness < 0:
            self.tiredness = 0

    def modify_stat(self, stat_name, amount):
        """
        Modifica el valor de un atributo específico de la entidad.
        """
        if stat_name in self.stats:
            self.stats[stat_name] += amount
            if self.stats[stat_name] < 0:
                self.stats[stat_name] = 0
    def modify_reputation(self, amount):
        """
        Modifica la reputación de la entidad.
        """
        self.reputation += amount
    def modify_weight(self, weight):
        """
        Modifica el peso de la entidad en kilogramos.
        """
        self.weight += weight
    def modify_height(self, height):
        """
        Modifica la altura de la entidad en centímetros.
        """
        self.height += height
    def update_needs(self, time_passed, hunger_decrease, thirst_decrease, tiredness_decrease, magic_heat_decrease):
        """
        Actualiza las necesidades de la entidad (hambre, sed, cansancio, calor mágico).
        """
        self.hunger = max(0, min(100, self.hunger - hunger_decrease * time_passed))
        self.thirst = max(0, min(100, self.thirst - thirst_decrease * time_passed))
        self.tiredness = max(0, min(100, self.tiredness - tiredness_decrease * time_passed))
        self.magic_heat = max(0, min(self.max_magic_heat, self.magic_heat - magic_heat_decrease * time_passed))


    def change_state(self, new_state):
        """
        Cambia el estado de la entidad.
        """
        self.state = new_state