from pydantic import BaseModel
from typing import List, Union, Literal

# Base operation with shorter names
class Op(BaseModel):
    type: str

class Chat(Op):
    type: Literal["chat", "message"]
    content: str

class Create(Op):
    type: Literal["create_file"]
    path: str
    content: str

class Edit(Op):
    type: Literal["edit_file"]
    path: str
    content: str

class Delete(Op):
    type: Literal["delete_file"]
    path: str

class Rename(Op):
    type: Literal["rename_file"]
    old_path: str
    new_path: str

class MkDir(Op):
    type: Literal["create_directory"]
    path: str

class RmDir(Op):
    type: Literal["delete_directory"]
    path: str

class Exec(Op):
    type: Literal["execute_command"]
    command: str

# Simplified Union without Annotated to reduce name length
AnyOp = Union[Chat, Create, Edit, Delete, Rename, MkDir, RmDir, Exec]

class OpsList(BaseModel):
    ops: List[AnyOp]

    class Config:
        title = "OpsList"  # Shorter title within the allowed length
