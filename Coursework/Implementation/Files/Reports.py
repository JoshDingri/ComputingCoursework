from appy.pod.renderer import Renderer
  
staff = [{'firstName': 'Delannay', 'name': 'Gaetan', 'age': 112},
         {'firstName': 'Gauthier', 'name': 'Bastien', 'age': 5},
         {'firstName': 'Jean-Michel', 'name': 'Abe', 'age': 79}]
  
renderer = Renderer('SimpleTestOds.ods', globals(), 'result.ods')
renderer.run()
