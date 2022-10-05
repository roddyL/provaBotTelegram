# !/code/smactbot/models/Gallery.py
# Authors:
#     Alberto
#     Loris

# libraries
import copy

# the class Gallery
class Gallery():
    """This class contains -- da finire
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
        self.the_query=the_query
        self.pos=int(0)
        self.size=len(the_query)
        self.isDeleting=False
        self.isReadyDelete=False

    def isDeletingChange(self) -> None:
        """_summary_
        """
        self.isDeleting=not self.isDeleting
    
    def isReadyDeleteChange(self) -> None:
        """_summary_
        """
        self.isReadyDelete=not self.isReadyDelete

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
        if self.the_class().costruttore(self.the_query[self.pos]).delete_reservation():
            self.the_query.pop(self.pos)
            self.isDeletingChange()
            self.isReadyDeleteChange()
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
        return self.the_class().constructor(self.the_query[self.pos]).show_to_gallery()
    
    def __repr__(self) -> str:
        return f"\nPos: {self.pos}\nSize: {self.size}\n{self.the_query}"