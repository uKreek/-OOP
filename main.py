from event_class import CoffeeClubMember, MukbangEnjoyer, Validator, Logger

validator = Validator()
logger = Logger()

Vladislav = CoffeeClubMember('Vladislav', 'coffee', 'potato')

Vladislav.property_changing += validator
Vladislav.property_changed += logger

Vladislav.name = 'Sergey'
Vladislav.favorite_drink = 'still_water'
Vladislav.favorite_food = 'peace'

Santana = MukbangEnjoyer('Santana', 'NikocadoAvocado', 'pasta')

Vladislav.property_changing += validator
Vladislav.property_changed += logger

Santana.name = ''
Santana.favorite_blogger = 'Lololowka'
Santana.favorite_food = 'burger'
