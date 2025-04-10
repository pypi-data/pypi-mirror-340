from fastapi_global_variable import GlobalVariable


class FastApiMicroservice:
  @staticmethod
  def config(env: str):
    return FastApiMicroservice(env)

  def __init__(self, env: str = 'LOCAL'):
    GlobalVariable.set('env', env.upper())
