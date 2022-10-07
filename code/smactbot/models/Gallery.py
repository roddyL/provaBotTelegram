# !/code/smactbot/models/Gallery.py
# Authors:
#     Alberto
#     Loris

# the class Gallery
class Gallery():
    """This class contains a generic gallery where each node contains
    a generic object where class is indicated with the attribute 'the
    _class'. All the objects in the gallery needs to belong to 'the_ 
    class'.
    """
    
    def __init__(
        self, 
        the_class,
        the_query: list[dict]=None
    ):
        """It initialize the object gallery, using a class 
        and a query

        Args:
            the_class (class): the class of each node of the gallery
            the_query (list[dict], optional): the list of fields that 
            needs to be manipulated by the class. Defaults to None to 
            indicate there is no nodes.
        """
        self.the_class=the_class
        """Class: this is the nature type of each node in the gallery"""
        self.the_query=the_query
        """List[dict]: this is a list of tuple from the db"""
        self.pos=int(0)
        """Int: this is the pointer of the gallery"""
        self.size=len(the_query)
        """Int: the size of the gallery"""
        self.user_want_to_delete=False
        """Bool: False until the user don't press delete to the node, 
        True when the user press the delete button
        """
        self.is_ready_to_delete=False
        """Bool: if the user confirm the choice to delete the node, it
        will be set to True, and the deleting action on the db will happen
        """

    def user_want_to_delete_change(self) -> None:
        """Change the status of the var user_want_to_delete
        """
        self.user_want_to_delete=not self.user_want_to_delete
    
    def is_ready_to_delete_change(self) -> None:
        """Change the status of the var is_ready_to_delete
        """
        self.is_ready_to_delete=not self.is_ready_to_delete

    def next(self) -> None:
        """It goes to the next node
        """
        if self.pos<self.size-1:
            self.pos+=1

    def back(self) -> None:
        """It goes to the previous node
        """
        if self.pos>0:
            self.pos-=1

    def delete(self) -> bool:
        """Before deleting the node, it use the delete method of the class

        Returns:
            bool: True if it has worked, False otherwise
        """
        if self.the_class().gallery_item_constructor(self.the_query[self.pos]).delete_reservation():
            self.the_query.pop(self.pos)
            self.user_want_to_delete_change()
            self.is_ready_to_delete_change()
            self.size-=1
            if self.pos!=0:
                self.pos-=1
                
            return True
        else:
            return False

    def show(self) -> str:
        """it show as string the info about the node 

        Returns:
            str: the info that object want to give with show_to_gallery
        """
        return self.the_class().gallery_item_constructor(self.the_query[self.pos]).show_to_gallery()
    
    def __repr__(self) -> str:
        return f"\nPos: {self.pos}\nSize: {self.size}\n{self.the_query}"