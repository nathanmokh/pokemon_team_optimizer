import pokebase as pb
from pokebase import cache

load_dotenv()

chesto = pb.APIResource('berry', 'chesto')
print(chesto)