from os import environ
from pydantic import BaseModel
from configue import ConFigue,ConFigueManager



class PydanticModelTest(BaseModel):
    key1:dict[str,int]
    key2:float

class ConFigue1Test(ConFigue):
    TEST_CONFIG_KEY="test_value"
    TEST_CONFIG_KEY_2=2
    TEST_CONFIG_KEY_3=["1","2"]
    TEST_CONFIG_KEY_4=PydanticModelTest(key1={"k1":1,"k2":2},key2=1.2)
    
class ConFigue2Test(ConFigue):
    TEST_CONFIG_KEY="test_value2"
    TEST_CONFIG_KEY_2=3
    TEST_CONFIG_KEY_3=[]
    TEST_CONFIG_KEY_4=PydanticModelTest(key1={"k1":8},key2=5.0)

class ConfigueManagerTest(ConFigueManager):
    TEST_CONFIG_KEY:str
    TEST_CONFIG_KEY_2:int
    TEST_CONFIG_KEY_3:list[str]
    TEST_CONFIG_KEY_4:PydanticModelTest

SELECTOR_KEY="TEST_CONFIGUE"
DEFAULT_CONFIGUES={"1":ConFigue1Test(),"2":ConFigue2Test()}
    
def configue_selector(configues:dict[str,ConFigue])->ConFigue:
    """Select the ConFigue object based on env variable"""
    return configues.get(environ.get(SELECTOR_KEY,"2"))
