import src.back.pokemon.hash_ring as hash_ring

def test_cards():
    assert hash_ring.all_cards.count()!=0

def test_hash_ring_nodes():
    print(hash_ring.hr.size)
    assert hash_ring.hr.size!=0

def test_get_hash_ring_node():
    current_node=hash_ring.hr.get_node_and_avaliability()
    present=current_node[1]
    print(present)
    assert present