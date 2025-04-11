import networkx as nx

import loman.visualization
from loman import Computation, States
import loman.computeengine
from collections import namedtuple
from loman.consts import SystemTags


def test_simple():
    comp = Computation()
    comp.add_node('a')
    comp.add_node('b', lambda a: a + 1)
    comp.add_node('c', lambda a: 2 * a)
    comp.add_node('d', lambda b, c: b + c)

    v = loman.visualization.GraphView(comp)

    nodes = v.viz_dot.obj_dict['nodes']
    label_to_name_mapping = {v[0]['attributes']['label']: k for k, v in nodes.items()}
    node = {label: nodes[name][0] for label, name in label_to_name_mapping.items()}
    assert node['a']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UNINITIALIZED]
    assert node['a']['attributes']['style'] == 'filled'
    assert node['b']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UNINITIALIZED]
    assert node['b']['attributes']['style'] == 'filled'
    assert node['c']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UNINITIALIZED]
    assert node['c']['attributes']['style'] == 'filled'
    assert node['d']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UNINITIALIZED]
    assert node['d']['attributes']['style'] == 'filled'

    comp.insert('a', 1)

    v.refresh()
    nodes = v.viz_dot.obj_dict['nodes']
    label_to_name_mapping = {v[0]['attributes']['label']: k for k, v in nodes.items()}
    node = {label: nodes[name][0] for label, name in label_to_name_mapping.items()}
    assert node['a']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UPTODATE]
    assert node['a']['attributes']['style'] == 'filled'
    assert node['b']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.COMPUTABLE]
    assert node['b']['attributes']['style'] == 'filled'
    assert node['c']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.COMPUTABLE]
    assert node['c']['attributes']['style'] == 'filled'
    assert node['d']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.STALE]
    assert node['d']['attributes']['style'] == 'filled'

    comp.compute_all()

    v.refresh()
    nodes = v.viz_dot.obj_dict['nodes']
    label_to_name_mapping = {v[0]['attributes']['label']: k for k, v in nodes.items()}
    node = {label: nodes[name][0] for label, name in label_to_name_mapping.items()}
    assert node['a']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UPTODATE]
    assert node['a']['attributes']['style'] == 'filled'
    assert node['b']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UPTODATE]
    assert node['b']['attributes']['style'] == 'filled'
    assert node['c']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UPTODATE]
    assert node['c']['attributes']['style'] == 'filled'
    assert node['d']['attributes']['fillcolor'] == loman.visualization.ColorByState.DEFAULT_STATE_COLORS[States.UPTODATE]
    assert node['d']['attributes']['style'] == 'filled'


def test_with_groups():
    comp = Computation()
    comp.add_node('a', group='foo')
    comp.add_node('b', lambda a: a + 1, group='foo')
    comp.add_node('c', lambda a: 2 * a, group='bar')
    comp.add_node('d', lambda b, c: b + c, group='bar')
    v = loman.visualization.GraphView(comp)

def test_show_expansion():
    Coordinate = namedtuple('Coordinate', ['x', 'y'])
    comp = Computation()
    comp.add_node('c', value=Coordinate(1, 2))
    comp.add_node('foo', lambda x: x + 1, kwds={'x': 'c.x'})
    comp.add_named_tuple_expansion('c', Coordinate)
    comp.compute_all()

    node_formatter = loman.visualization.NodeFormatter.create()

    view_uncontracted = loman.visualization.GraphView(comp, node_formatter=node_formatter)
    view_uncontracted.refresh()
    labels = nx.get_node_attributes(view_uncontracted.viz_dag, 'label')
    assert set(labels.values()) == {'c', 'c.x', 'c.y', 'foo'}

    nodes_to_contract = comp.nodes_by_tag(SystemTags.EXPANSION)
    view_contracted = loman.visualization.GraphView(comp, node_formatter=node_formatter, nodes_to_contract=nodes_to_contract)
    view_contracted.refresh()
    labels = nx.get_node_attributes(view_contracted.viz_dag, 'label')
    assert set(labels.values()) == {'c', 'foo'}
