from py_d2.D2Connection import D2Connection
from py_d2.D2Diagram import D2Diagram
from py_d2.D2Shape import D2Shape
from py_d2.D2Style import D2Style
import asyncio

shapes = []


async def test2():
    print("Contructing a simple graph...")
    shapes.append(D2Shape(name="shape_name1", style=D2Style(fill="red")))
    shapes.append(D2Shape(name="shape_name1", style=D2Style(fill="red")))
    shapes.remove(str(D2Shape(name="shape_name1", style=D2Style(fill="red"))))
    print(shapes)
    connections = [D2Connection(shape_1="shape_name1", shape_2="shape_name2")]

    diagram = D2Diagram(shapes=shapes, connections=connections)
    return diagram


async def test():
    result_test = await test2()
    print(result_test)
    print("Writing graph to file...")
    with open("graph.d2", "w") as f:
        f.write(str(result_test))
        print("Done! (graph.d2)")
    return result_test


loop = asyncio.get_event_loop()
result = loop.run_until_complete(test())
print(result)
